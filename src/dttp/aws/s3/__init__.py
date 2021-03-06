from io import BytesIO
import io
import boto3
import logging
import json
import os

logger = logging.getLogger()
SECRET_JSON_LOC = './secret.json'

class AWSS3:

    def __init__(self, bucket=None):
        if(os.path.isfile(SECRET_JSON_LOC)):
            with open(SECRET_JSON_LOC, "r") as json_file:
                self.__bucket_name = bucket if bucket else json.load(json_file)['bucketName']
        else:
            self.__bucket_name = bucket if bucket else None
        self.__s3 = boto3.resource('s3')
        self.__client = boto3.client('s3')

    def print_all_buckets(self):
        for bucket in self.__s3.buckets.all():
            print(bucket.name)

    def save_to_bucket(self, file_in, folder=None, bucket=None):
        bucket_name = bucket if bucket else self.__bucket_name
        if not file_in.name:
            raise Exception('no name attribute in file')
        if not bucket_name:
            raise Exception('Bucket name not defined')
        file_name = file_in.name
        self.__client.upload_fileobj(file_in, bucket_name, folder + '/' + file_name if folder else file_name)


    def delete_obj(self, key, bucket=None):
        bucket_name = bucket if bucket else self.__bucket_name
        obj = self.__s3.Object(bucket_name, key)
        obj.delete()

    # @param bucket - name of bucket
    # @param key = file key
    # @return returns files bin data
    def get_obj_bin(self, key, bucket=None):
        bucket_name = bucket if bucket else self.__bucket_name
        logger.critical('Reading {} from {}'.format(key, bucket_name))
        obj = self.__client.get_object(Bucket=bucket_name, Key=key)
        file = BytesIO(obj['Body'].read())
        file.name = key
        return file

# if __name__ == '__main__':
#     file = open('../../../chartzipurls.txt', 'rb')
#     AWSS3().save_to_bucket(file, 'dttp_zipfiles')

