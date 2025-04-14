provider "aws" {
  region = "ap-south-1"
}

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_execution_role" {
  name               = "lambda_execution_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "ec2_policy_attachment" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
}

# --- Lambda Functions ---

# Stop Idle EC2 Instances
resource "aws_lambda_function" "stop_idle_ec2" {
  function_name    = "StopIdleInstances"
  filename         = "${path.module}/lambda/stop-idle-instances.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/stop-idle-instances.zip")
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = "stop-idle-instances.lambda_handler"
  runtime          = "python3.8"
}

# Delete Unattached EBS Volumes
resource "aws_lambda_function" "delete_unattached_ebs" {
  function_name    = "DeleteUnattachedEBS"
  filename         = "${path.module}/lambda/delete_unattached_ebs.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/delete_unattached_ebs.zip")
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = "delete_unattached_ebs.lambda_handler"
  runtime          = "python3.8"
}

# Release Unused Elastic IPs
resource "aws_lambda_function" "release_unused_eip" {
  function_name    = "ReleaseUnusedEIPs"
  filename         = "${path.module}/lambda/release_unused_eips.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/release_unused_eips.zip")
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = "release_unused_eips.lambda_handler"
  runtime          = "python3.8"
}

