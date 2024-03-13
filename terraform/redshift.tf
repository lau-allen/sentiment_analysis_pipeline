#random password for redshift resource 
resource "random_password" "password" {
  length           = 16
  special          = true
  override_special = "!$%&*()-_=+[]{}<>:?"
}

#create redshift cluster resource 
resource "aws_redshift_cluster" "redshift_cluster" {
  cluster_identifier  = var.redshift_cluster_name
  database_name       = var.redshift_db_name
  master_username     = var.redshift_master_username
  master_password     = random_password.password.result
  node_type           = var.redshift_node_type
  cluster_type        = var.redshift_cluster_type
  skip_final_snapshot = true
  vpc_security_group_ids = [aws_security_group.redshift_sg.id]
}

#create secret in AWS secret manager for Redshift connection details 
resource "aws_secretsmanager_secret" "redshift_connection" {
  description             = "Redshift connect details"
  name                    = var.redshift_secret_name
  recovery_window_in_days = 0
}

#define secret information 
resource "aws_secretsmanager_secret_version" "redshift_connection" {
  secret_id = aws_secretsmanager_secret.redshift_connection.id
  secret_string = jsonencode({
    username            = aws_redshift_cluster.redshift_cluster.master_username
    password            = aws_redshift_cluster.redshift_cluster.master_password
    engine              = "redshift"
    host                = aws_redshift_cluster.redshift_cluster.endpoint
    port                = "5439"
    dbClusterIdentifier = aws_redshift_cluster.redshift_cluster.cluster_identifier
    db_name = aws_redshift_cluster.redshift_cluster.database_name
  })
}
