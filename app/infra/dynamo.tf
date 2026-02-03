resource "aws_dynamodb_table" "tasks_table" {
  name           = "${var.project_name}-db"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Project = var.project_name
  }
}