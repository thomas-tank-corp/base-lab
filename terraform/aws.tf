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