import boto3  # import Boto3


def scan_devices(display_devices_data, dynamodb=None):
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:8000")
    # Specify the table to scan
    devices_table = dynamodb.Table('SmartFarming')
    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = devices_table.scan()
        display_devices_data(response.get('Items', []))
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None


if __name__ == '__main__':
    # A method for printing the items
    def print_devices(devices):
        for device in devices:
            print(f"\n{device['device_id']} device")
            print('\nTemperature Information')
            print(device['temperature_info'])
            print('\nHumidity Information')
            print(device['humidity_info'])            

    print(
        f"Fetching all IOT devices data")
    # Print the items returned
    scan_devices(print_devices)