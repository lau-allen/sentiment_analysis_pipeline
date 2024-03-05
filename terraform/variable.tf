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