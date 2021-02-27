import boto3
import json


class AWSS3:

    def __init__(self):
        with open('./secret.json', "r") as json_file:
            self.__bucket_name = json.load(json_file)['bucketName']
        self.__s3 = boto3.resource('s3')
        self.__client = boto3.client('s3')

    def print_all_buckets(self):
        for bucket in self.__s3.buckets.all():
            print(bucket.name)

    def save_to_bucket(self, file_in, folder=None, bucket=None):
        bucket_name = bucket if bucket else self.__bucket_name
        file_name = file_in.name
        self.__client.upload_fileobj(file_in, bucket_name, folder + '/' + file_name if folder else file_name)


if __name__ == '__main__':
    file = open('chartzipurls.txt', 'rb')
    AWSS3().save_to_bucket(file, 'dttp_zipfiles')
