# import Boto3 exceptions and error handling module
from botocore.exceptions import ClientError
import boto3  # import Boto3


def get_device(device_id,dynamodb=None):
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:8000")
    # Specify the table to read from
    devices_table = dynamodb.Table('SmartFarming')

    try:
        response = devices_table.get_item(
            Key={'device_id': device_id})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']


def average_temp(device):
    # Print the data read
    temp = device['temperature_info']
    location = device['location']
    iot = device['device_id']
    temp_sum=0
    total_items = 0
    for i in temp:
        temp_sum += temp[i]
        total_items+=1
    avg_temp = temp_sum/total_items
    if avg_temp > 25:
        print(f'Average temperature in {iot} device on location {location} is {avg_temp} (sprinklers should be on!)')
    else:
        print(f'Average temperature in {iot} device on location {location} is {avg_temp}')
            


if __name__ == '__main__':
    iot_devices = ['iot1','iot2','iot3','iot4']
    for i in iot_devices:
        device = get_device(i)
        if device:
            average_temp(device)

