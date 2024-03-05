#define IAM user for s3 workflows 
resource "aws_iam_user" "sap_s3_user" {
  name = var.s3_user
}

#define policy document for s3 user 
data "aws_iam_policy_document" "sap_s3_permissions" {
  statement {
    effect    = "Allow"
    actions   = ["s3:PutObject", "s3:GetObject", "s3:ListBucket"]
    resources = ["arn:aws:s3:::${var.s3_bucket_name}/*"]
  }
}

#define policy from policy document and attach to user 
resource "aws_iam_user_policy" "sap_s3_policy" {
  name   = var.s3_policy
  user   = aws_iam_user.sap_s3_user.name
  policy = data.aws_iam_policy_document.sap_s3_permissions.json
}