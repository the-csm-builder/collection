version = 0.1
[default]
[default.deploy]
[default.deploy.parameters]
stack_name = "sam-app"
s3_bucket = "aws-sam-cli-managed-default-samclisourcebucket-1t07fv8fcdeas"
s3_prefix = "sam-app"
region = "us-east-1"
confirm_changeset = true
capabilities = "CAPABILITY_IAM"
image_repositories = []

[personal]
[personal.deploy]
[personal.deploy.parameters]
stack_name = "content-collection"
s3_bucket = "aws-sam-cli-managed-default-samclisourcebucket-11vns34sasgrg"
s3_prefix = "content-collection"
region = "us-east-1"
profile = "personal"
confirm_changeset = true
capabilities = "CAPABILITY_IAM"
image_repositories = []
