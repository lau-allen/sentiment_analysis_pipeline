variable "aws_region" {
  description = "AWS service region"
  type        = string
  default     = "us-east-1"
}

variable "s3_bucket_name" {
  description = "Name for AWS S3 bucket"
  type        = string
  default     = "sap-webscrape-extract"
}

variable "s3_user" {
  description = "Name for AWS IAM User to work with s3 buckets"
  type        = string
  default     = "sap-s3-user"
}

variable "s3_policy" {
  description = "Name for AWS IAM Policy to work with s3 buckets"
  type        = string
  default     = "sap-s3-policy"
}

variable "redshift_db_name" {
  type = string 
  description = "Defined name for database in Redshift"
  default = "sap_db"
}

variable "redshift_master_username" {
  type = string
  description = "Defined username"
}

variable "redshift_node_type" {
  type = string
  description = "Node type for Redshift cluster"
  default = "dc2.large"
}

variable "redshift_cluster_type" {
  type = string
  description = "Cluster type for Redshift cluster"
  default = "single-node"
}

variable "redshift_cluster_name" {
  type = string
  description = "Cluster name"
  default = "sap-redshift-cluster"
}

variable "redshift_secret_name" {
  type = string
  description = "Redshift secret name for storing information to connect via redshift_connector"
  default = "sap_redshift_secret"
}

## below code sourced from https://github.com/PrefectHQ/prefect-recipes/tree/main/devops/infrastructure-as-code/aws/tf-prefect2-ecs-agent
variable "agent_cpu" {
  description = "CPU units to allocate to the agent"
  default     = 1024
  type        = number
}

variable "agent_desired_count" {
  description = "Number of agents to run"
  default     = 1
  type        = number
}

variable "agent_extra_pip_packages" {
  description = "Packages to install on the agent assuming image is based on prefecthq/prefect"
  default     = "prefect-aws s3fs"
  type        = string
}

variable "agent_image" {
  description = "Container image for the agent. This could be the name of an image in a public repo or an ECR ARN"
  default     = "prefecthq/prefect:2-python3.10-conda"
  type        = string
}

variable "agent_log_retention_in_days" {
  description = "Number of days to retain agent logs for"
  default     = 30
  type        = number
}

variable "agent_memory" {
  description = "Memory units to allocate to the agent"
  default     = 2048
  type        = number
}

variable "agent_queue_name" {
  description = "Prefect queue that the agent should listen to"
  default     = "default"
  type        = string
}

variable "agent_subnets" {
  description = "Subnets to place the agent in"
  type        = list(string)
}

variable "agent_task_role_arn" {
  description = "Optional task role ARN to pass to the agent. If not defined, a task role will be created"
  default     = null
  type        = string
}

variable "name" {
  description = "Unique name for this agent deployment"
  type        = string
}

variable "prefect_account_id" {
  description = "Prefect cloud account ID"
  type        = string
}

variable "prefect_workspace_id" {
  description = "Prefect cloud workspace ID"
  type        = string
}

variable "prefect_api_key" {
  description = "Prefect cloud API key"
  type        = string
  sensitive   = true
}

variable "vpc_id" {
  description = "VPC ID in which to create all resources"
  type        = string
}

variable "secrets_manager_recovery_in_days" {
  type        = number
  default     = 30
  description = "Deletion delay for AWS Secrets Manager upon resource destruction"
}