resource "aws_security_group" "prefect_agent" {
  name        = "prefect-agent-sg-${var.name}"
  description = "ECS Prefect Agent"
  vpc_id      = var.vpc_id
}

resource "aws_security_group" "redshift_sg" {
  name = "redshift-cluster-sg"
  description = "Redshift Cluster SG"
  vpc_id = var.vpc_id
}

resource "aws_security_group_rule" "https_outbound" {
  // S3 Gateway interfaces are implemented at the routing level which means we
  // can avoid the metered billing of a VPC endpoint interface by allowing
  // outbound traffic to the public IP ranges, which will be routed through
  // the Gateway interface:
  // https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html
  description       = "HTTPS outbound"
  type              = "egress"
  security_group_id = aws_security_group.prefect_agent.id
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]

}

#defining egress rule for ECS to allow outbound traffic to redshift point 
resource "aws_security_group_rule" "redshift_outbound" {
  type = "egress"
  security_group_id = aws_security_group.prefect_agent.id
  from_port = 5439
  to_port = 5439
  protocol = "tcp" 
  cidr_blocks = ["0.0.0.0/0"]
}

#defining ingress rule for Redshift to allow inbound traffic 
resource "aws_security_group_rule" "redshift_inbound" {
  type = "ingress"
  security_group_id = aws_security_group.redshift_sg.id
  from_port = 5439
  to_port = 5439
  protocol = "tcp"
  source_security_group_id = aws_security_group.prefect_agent.id
}