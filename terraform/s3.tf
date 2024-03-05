#create s3 bucket with defined name 
resource "aws_s3_bucket" "sentiment_analysis_bucket" {
  #defined name 
  bucket = var.s3_bucket_name
  #all objects should be deleted when bucket is destroyed 
  force_destroy = true
}