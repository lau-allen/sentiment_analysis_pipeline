##reference: https://github.com/PrefectHQ/prefect-recipes/tree/main/devops/infrastructure-as-code/aws/tf-prefect2-ecs-agent
output "prefect_agent_service_id" {
  value = aws_ecs_service.prefect_agent_service.id
}

output "prefect_agent_execution_role_arn" {
  value = aws_iam_role.prefect_agent_execution_role.arn
}

output "prefect_agent_task_role_arn" {
  value = var.agent_task_role_arn == null ? aws_iam_role.prefect_agent_task_role[0].arn : var.agent_task_role_arn
}

output "prefect_agent_security_group" {
  value = aws_security_group.prefect_agent.id
}

output "prefect_agent_cluster_name" {
  value = aws_ecs_cluster.prefect_agent_cluster.name
}

output "vpc_id" {
  value = var.vpc_id
}