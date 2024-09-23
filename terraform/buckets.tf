resource "aws_s3_bucket" "prod_datalake_artifacts" {
  bucket = "prod-datalake-artifacts"
  force_destroy = true

  tags = {
    Name        = "Artifacts bucket"
    Environment = "Prod"
  }
}

resource "aws_s3_bucket" "prod_bronze_datalake" {
  bucket = "prod-brz-datalake"
  force_destroy = true
  
  tags = {
    Name        = "Bronze Datalake Bucket"
    Environment = "Prod"
  }
}

resource "aws_s3_bucket" "prod_silver_datalake" {
  bucket = "prod-silver-datalake"
  force_destroy = true
  
  tags = {
    Name        = "Silver Datalake Bucket"
    Environment = "Prod"
  }
}

resource "aws_s3_bucket" "prod_gold_datalake" {
  bucket = "prod-gold-datalake"
  force_destroy = true
  
  tags = {
    Name        = "Gold Datalake Bucket"
    Environment = "Prod"
  }
}