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
    k8_lb_ip = os.environ['K8_DEV_INGRESS_IP']
    k8_gcpprojectid = os.environ ['INSTRUQT_GCP_PROJECT_GCP_PROJECT_PROJECT_ID']
    k8_gcpzone = os.environ ['TF_VAR_GCP_ZONE']
except Exception as e:
    print(f"Error: Could not read {e} from environment.")
    print(f"Please export {e} as environment variable.")
    sys.exit()

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
        "username": f"{aws_username}",
        "password": f"{aws_password}"     
      },
    "id" : f"{aws_id}",
    "name": f"{aws_id}",
    "type": "aws"
}
response = requests.request("POST", url, headers=headers, json=payload)
if response.status_code==200:
    print(f"The resource account has been registered.")
elif response.status_code==409:
    print(f"Unable to create resource account. Account with id aws-instruqt already exists.")
else:
    print(f"Unable to create resource account. POST {url} returned status code {response.status_code}.")


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
    print(f"The resource account has been registered.")
elif response.status_code==409:
    print(f"Unable to create resource account. Account with id already exists.")
else:
    print(f"Unable to create resource account. POST {url} returned status code {response.status_code}.")




# Register GKE Cluster
##########################################################
url = f"https://{humanitec_url}/orgs/{humanitec_org}/resources/definitions"
payload = {
    "org_id": f"{humanitec_org}",
    "id": "kube-gcp-instruqt",
    "name": "kube-gcp-instruqt",
    "type": "k8s-cluster",
    "driver_type": "humanitec/k8s-cluster-gke",
    "driver_inputs": {
      "values": {
        "loadbalancer": f"{k8_lb_ip}",
        "name": "humanitec-k8-dev",
        "project_id": f"{k8_gcpprojectid}",
        "zone": f"{k8_gcpzone}"
      },
      "secrets" : {
        "credentials" f"{gcp_sa}"
      }
    }
}

response = requests.request("POST", url, headers=headers, json=payload)
if response.status_code==200:
    print(f"The resource definition has been registered.")
else:
    print(f"Unable to create resource account. POST {url} returned status code {response.status_code}.")
