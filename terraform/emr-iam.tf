resource "aws_iam_role" "emr_role" {
  name = "emr-role"
  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "EMRServerlessTrustPolicy",
        "Action": "sts:AssumeRole",
        "Effect": "Allow",
        "Principal": {
            "Service": "emr-serverless.amazonaws.com"
        }
    }]
}
EOF
}

resource "aws_iam_policy" "emr_policy" {
  name = "emr-policy"
  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ReadAccessForEMRSamples",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::*.elasticmapreduce",
                "arn:aws:s3:::*.elasticmapreduce/*"
            ]
        },
        {
            "Sid": "FullAccessToOutputBucket",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::prod-datalake-artifacts",
                "arn:aws:s3:::prod-datalake-artifacts/*",
                "arn:aws:s3:::prod-bronze-datalake",
                "arn:aws:s3:::prod-bronze-datalake/*",
                "arn:aws:s3:::prod-silver-datalake",
                "arn:aws:s3:::prod-silver-datalake/*",
                "arn:aws:s3:::prod-gold-datalake",
                "arn:aws:s3:::prod-gold-datalake/*",
            ]
        },
        {
            "Sid": "GlueCreateAndReadDataCatalog",
            "Effect": "Allow",
            "Action": [
                "glue:GetDatabase",
                "glue:CreateDatabase",
                "glue:GetDataBases",
                "glue:CreateTable",
                "glue:GetTable",
                "glue:UpdateTable",
                "glue:DeleteTable",
                "glue:GetTables",
                "glue:GetPartition",
                "glue:GetPartitions",
                "glue:CreatePartition",
                "glue:BatchCreatePartition",
                "glue:GetUserDefinedFunctions"
            ],
            "Resource": ["*"]
        }
    ]
})
}

resource "aws_iam_role_policy_attachment" "emr_role_policy_attach" {
  role       = aws_iam_role.emr_role.name
  policy_arn = aws_iam_policy.emr_policy.arn
}
output "emr_arn_role" {
  value = aws_iam_role.emr_role.arn
}