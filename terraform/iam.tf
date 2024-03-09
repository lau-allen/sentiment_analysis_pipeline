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

##reference: https://github.com/PrefectHQ/prefect-recipes/tree/main/devops/infrastructure-as-code/aws/tf-prefect2-ecs-agent
resource "aws_secretsmanager_secret" "prefect_api_key" {
  name                    = "prefect-api-key-${var.name}"
  recovery_window_in_days = var.secrets_manager_recovery_in_days
}

resource "aws_secretsmanager_secret_version" "prefect_api_key_version" {
  secret_id     = aws_secretsmanager_secret.prefect_api_key.id
  secret_string = var.prefect_api_key
}

resource "aws_iam_role" "prefect_agent_execution_role" {
  name = "prefect-agent-execution-role-${var.name}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ]
  })

  inline_policy {
    name = "ssm-allow-read-prefect-api-key-${var.name}"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "kms:Decrypt",
            "secretsmanager:GetSecretValue",
            "ssm:GetParameters"
          ]
          Effect = "Allow"
          Resource = [
            aws_secretsmanager_secret.prefect_api_key.arn
          ]
        }
      ]
    })
  }
  inline_policy {
    name = "logs-allow-create-log-group-${var.name}"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "logs:CreateLogGroup",
          ]
          Effect   = "Allow"
          Resource = "*"
        }
      ]
    })
  }
  // AmazonECSTaskExecutionRolePolicy is an AWS managed role for creating ECS tasks and services
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"]
}

resource "aws_iam_role" "prefect_agent_task_role" {
  name  = "prefect-agent-task-role-${var.name}"
  count = var.agent_task_role_arn == null ? 1 : 0

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ]
  })

  inline_policy {
    name = "prefect-agent-allow-ecs-task-${var.name}"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "ec2:DescribeSubnets",
            "ec2:DescribeVpcs",
            "ecr:BatchCheckLayerAvailability",
            "ecr:BatchGetImage",
            "ecr:GetAuthorizationToken",
            "ecr:GetDownloadUrlForLayer",
            "ecs:DeregisterTaskDefinition",
            "ecs:DescribeTasks",
            "ecs:RegisterTaskDefinition",
            "ecs:RunTask",
            "ecs:StopTask",
            "ecs:TagResource",
            "iam:PassRole",
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:GetLogEvents",
            "logs:PutLogEvents"
          ]
          Effect   = "Allow"
          Resource = "*"
        }
      ]
    })
  }
}