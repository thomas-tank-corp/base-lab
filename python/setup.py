#!/usr/bin/env python3

import requests
import os
import sys
import time
import json

try:
    humanitec_token = os.environ['HUMANITEC_TOKEN']
    humanitec_org = os.environ['HUMANITEC_ORG']
    aws_username = os.environ['INSTRUQT_AWS_ACCOUNT_AWS_ACCOUNT_USERNAME']
    aws_password = os.environ['INSTRUQT_AWS_ACCOUNT_AWS_ACCOUNT_PASSWORD']
    aws_id = os.environ['INSTRUQT_AWS_ACCOUNT_AWS_ACCOUNT_USERNAME']
    gcp_username = os.environ['INSTRUQT_GCP_PROJECT_GCP_PROJECT_USER_EMAIL']
    gcp_password = os.environ['INSTRUQT_GCP_PROJECT_GCP_PROJECT_USER_PASSWORD']
    gcp_id = os.environ['INSTRUQT_GCP_PROJECT_GCP_PROJECT_PROJECT_ID']
    gcp_sa = os.environ['GCP_SA']
    gke_endpoint = os.environ['GKE_ENDPOINT']
    k8_gcpprojectid = os.environ ['INSTRUQT_GCP_PROJECT_GCP_PROJECT_PROJECT_ID']
    k8_gcpzone = os.environ ['GOOGLE_ZONE']
    aws_key = os.environ ['INSTRUQT_AWS_ACCOUNT_AWS_ACCOUNT_AWS_ACCESS_KEY_ID']
    aws_secret = os.environ ['INSTRUQT_AWS_ACCOUNT_AWS_ACCOUNT_AWS_SECRET_ACCESS_KEY']
    eks_endpoint = os.environ ['EKS_ENDPOINT'] 
    random = os.environ ['RANDOM_TF']
    sql_usr = os.environ ['SQL_USR']
    sql_pass = os.environ ['SQL_PASS']
    sql_connection = os.environ['SQL_CONNECTION']
    
    # gke_payload = os.environ['GKE_PAYLOAD']
    # azure_client_id = os.environ ['RANDOM']
    # azure_client_secret = os.environ ['RANDOM']
    # azure_subscription_id = os.environ ['RANDOM']
    # azure_tenant_id = os.environ ['RANDOM']
    # aks_endpoint = os.environ ['RANDOM']


except Exception as e:
    print(f"Error: Could not read {e} from environment.")
    print(f"Please export {e} as environment variable.")


humanitec_url = "api.humanitec.io"

headers = {
    'Authorization': f'Bearer {humanitec_token}',
    'Content-Type': 'application/json'
}


# Register AWS Resource Account 
##########################################################
url = f"https://{humanitec_url}/orgs/{humanitec_org}/resources/accounts"
payload = {
    "credentials": {
        "access_key_id": f"{aws_key}",
        "secret_key_id": f"{aws_secret}"     
      },
    "id" : f"{aws_id}",
    "name": f"{aws_id}",
    "type": "aws"
}
response = requests.request("POST", url, headers=headers, json=payload)
if response.status_code==200:
    print(f"The resource AWS account has been registered.")
elif response.status_code==409:
    print(f"Unable to create AWS resource account. Account with id aws-instruqt already exists.")
else:
    print(f"Unable to create AWS resource account. POST {url} returned status code {response.status_code}.")


# Register GCP Resource Account 
##########################################################
url = f"https://{humanitec_url}/orgs/{humanitec_org}/resources/accounts"
payload = {
    "credentials": {
        "username": f"{gcp_username}",
        "password": f"{gcp_password}"     
      },
    "id" : f"{gcp_id}",
    "name": f"{gcp_id}",
    "type": "gcp"
}
response = requests.request("POST", url, headers=headers, json=payload)
if response.status_code==200:
    print(f"The GCP account has been registered.")
elif response.status_code==409:
    print(f"Unable to create GCP resource account. Account with id already exists.")
else:
    print(f"Unable to create GCP resource account. POST {url} returned status code {response.status_code}.")




# Register GKE Cluster
##########################################################
# url = f"https://{humanitec_url}/orgs/{humanitec_org}/resources/defs"
# payload = f"{gke_payload}"

# response = requests.request("POST", url, headers=headers, json=payload)
# if response.status_code==200:
#     print(f"The resource GKE resource definition has been registered.")
# else:
#     print(f"Unable to create GKE resource account. POST {url} returned status code {response.status_code}.")

# Register EKS Cluster
##########################################################
url = f"https://{humanitec_url}/orgs/{humanitec_org}/resources/defs"
payload = {
    "id": f"eks-{random}",
    "name": f"eks-{random}",
    "type": "k8s-cluster",
    "driver_type": "humanitec/k8s-cluster-eks",
    "driver_inputs": {
      "secrets": {
         "credentials": {
            "aws_access_key_id": f"{aws_key}",
            "aws_secret_access_key": f"{aws_secret}"
          }
      },
      "values": {
        "loadbalancer": f"{eks_endpoint}",
        "loadbalancer_hosted_zone": "eu-west-1",
        "name": "humanitec-eks",
        "region": "eu-west-1"
      }
    }
}

response = requests.request("POST", url, headers=headers, json=payload)
if response.status_code==200:
    print(f"The EKS resource definition has been registered.")
else:
    print(f"Unable to create EKS resource account. POST {url} returned status code {response.status_code}.")


#Register GCP CloudSQL
#########################################################

url = f"https://{humanitec_url}/orgs/{humanitec_org}/resources/defs"
payload = {
"id": f"postgres-{random}",
"name": f"postgres-{random}",
"type": "postgres",
"driver_type": "humanitec/postgres-cloudsql",
"driver_account": f"{gcp_id}",
"driver_inputs": {
  "secrets": {
    "dbcredentials": {
      "password": f"{sql_pass}",
      "username": f"{sql_usr}"
    }
  },
  "values": {
      "instance": f"{sql_connection}"
  }
 } 
}

response = requests.request("POST", url, headers=headers, json=payload)
if response.status_code==200:
    print(f"The resource CloudSQL definition has been registered.")
else:
    print(f"Unable to create CloudSQL resource account. POST {url} returned status code {response.status_code}.")


#Register Namespace
#########################################################

url = f"https://{humanitec_url}/orgs/{humanitec_org}/resources/defs"
payload = {
"id": "kube-namespace",
"name": "kube-namespace",
"type": "k8s-namespace",
"driver_type": "humanitec/static",
"driver_inputs": {
    "values": {
    "namespace": "${context.env.id}-env-${context.app.id}-app"
    }
  }
} 

response = requests.request("POST", url, headers=headers, json=payload)
if response.status_code==200:
    print(f"The Namespace resource definition has been registered.")
else:
    print(f"Unable to create Namepsace resource definition. POST {url} returned status code {response.status_code}.")


#Register AKS
#########################################################
# url = f"https://{humanitec_url}/orgs/{humanitec_org}/resources/defs"
# payload = {
#     "id": f"aks-humanitec-{random}",
#     "name": f"aks-humanitec-{random}",
#     "type": "k8s-cluster",
#     "driver_type": "humanitec/k8s-cluster-aks",
#     "driver_inputs": {
#       "values": {
#         "credentials":{
#             "ARM_CLIENT_ID" : f"{azure_client_id}",
#             "ARM_CLIENT_SECRET": f"{azure_client_secret}",
#             "ARM_SUBSCRIPTION_ID": f"{azure_subscription_id}",
#             "ARM_TENANT_ID": f"{azure_tenant_id}"      
#         },
#         "loadbalancer": f"{aks_endpoint}",
#         "loadbalancer_hosted_zone": "eu-west-1",
#         "name": "humanitec-eks",
#         "region": "eu-west-1"
#       }
#     }
# }
