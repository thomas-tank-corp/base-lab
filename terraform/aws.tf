locals {
  region = "eu-west-1"
}


module "vpc" {

  source  = "terraform-aws-modules/vpc/aws"
  version = "3.14.4"

  name = "humanitec-lab"
  cidr = "10.0.0.0/16"

  azs             = ["${local.region}a", "${local.region}b", "${local.region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_ipv6 = true

  enable_nat_gateway = false
  single_nat_gateway = true

  public_subnet_tags = {
    Name = "public-subnet"
  }

  tags = {
    Owner       = "hum-user"
    Environment = "dev"
  }

  vpc_tags = {
    Name = "humanitec-lab"
  }
}


module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 18.0"

  cluster_name    = "humanitec-eks"
  cluster_version = "1.22"

  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = true

 

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.public_subnets


 

  # EKS Managed Node Group(s)
  eks_managed_node_group_defaults = {
    disk_size      = 50
    instance_types = ["m6i.large", "m5.large", "m5n.large", "m5zn.large"]
  }

  eks_managed_node_groups = {
    blue = {}
    green = {
      min_size     = 1
      max_size     = 3
      desired_size = 3

      instance_types = ["t3.small"]
      capacity_type  = "SPOT"
    }
  }


  tags = {
    Environment = "dev"
    Terraform   = "true"
  }
}

module "security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 4.0"

  name        = "db_group"
  description = "Complete PostgreSQL example security group"
  vpc_id      = module.vpc.vpc_id

  # ingress
  ingress_with_cidr_blocks = [
    {
      from_port   = 5432
      to_port     = 5432
      protocol    = "tcp"
      description = "PostgreSQL access from within VPC"
      cidr_blocks = module.vpc.vpc_cidr_block
    },
  ]

  tags = "humanitec-dev-rds"
}


module "db" {
  source  = "terraform-aws-modules/rds/aws"
  version = "5.1.0"

  identifier = "RDS_POSTGRES"


  engine               = "postgres"
  engine_version       = "14.1"
  family               = "postgres14" 
  major_engine_version = "14"         
  instance_class       = "db.t4g.large"

  allocated_storage     = 20
  max_allocated_storage = 100

  # NOTE: Do NOT use 'user' as the value for 'username' as it throws:
  # "Error creating DB Instance: InvalidParameterValue: MasterUsername
  # user cannot be used as it is a reserved word used by the engine"
  db_name  = "RDS_POSTGRES"
  username = "postgresql"
  port     = 5432

  multi_az               = true
  db_subnet_group_name   = module.vpc.vpc_id
  vpc_security_group_ids = [module.security_group.security_group_id]

}