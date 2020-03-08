import boto3
import datetime
import os
from boto3.dynamodb.conditions import Attr
from EmailSender import EmailSender

class DataSaver:
    def __init__(self):
        self.aws_access_key_id = os.environ.get("ACCESS_KEY")
        self.aws_secret_access_key = os.environ.get("SECRET_ACCESS_KEY")
        self.region_name = os.environ.get("REGION_NAME")
        self.table = os.environ.get("TABLE_NAME")

    def save_request_info(self, message, result, exception):
        session = boto3.Session(aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key, region_name=self.region_name)
        dynamodb = session.resource('dynamodb')
        table = dynamodb.Table(self.table)
        self.check_if_new_user(table, message)
        table.put_item(
                Item={
                    "username" : f"{message.from_user.first_name} {message.from_user.last_name}",
                    "date" : format(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),
                    "message" : message.text,
                    "result" : result,
                    "error" : exception
                })

    def check_if_new_user(self, table, message):
        response = table.scan(
            FilterExpression=Attr('username').eq(f"{message.from_user.first_name} {message.from_user.last_name}"))
        if len(response["Items"]) == 0:
            email = EmailSender()
            email.send_new_user_email(message)


