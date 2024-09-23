import requests
import json
import boto3
import sys

def main(bucket_name : str, object_name :str):
    response = requests.get("https://api.openbrewerydb.org/breweries")

    send_to_s3(text=response.text, bucket_name=bucket_name, object_name=object_name)

def send_to_s3(text : str, bucket_name : str, object_name : str) :
    string_bytes = text.encode('utf-8')
    s3_client = boto3.client('s3')
    s3_client.put_object(Body=string_bytes, Bucket=bucket_name, Key=object_name)

if __name__ == "__main__":
    bucket_name = sys.argv[1]
    object_name = sys.argv[2]
    main()