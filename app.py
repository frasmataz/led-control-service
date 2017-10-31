from chalice import Chalice

app = Chalice(app_name='LEDControlService')
app.debug = True

def setup_dynamo():
    import boto3 
    dynamo = boto3.client('dynamodb')

    return dynamo


@app.route('/', methods=['GET'])
def get():
    dynamo = setup_dynamo()

    response = dynamo.get_item(
        TableName='led-control',
        Key={
            'device-id': {
                'N': '0'
            }
        }
    )

    return {
        'r': response['Item']['r']['N'],
        'g': response['Item']['g']['N'],
        'b': response['Item']['b']['N']
    }


@app.route('/', methods=['POST'], content_types=['application/json'])
def set():
    query_params = app.current_request.query_params
    r = query_params['r']
    g = query_params['g']
    b = query_params['b']

    dynamo = setup_dynamo()

    response = dynamo.update_item(
        TableName='led-control',
        Key={
            'device-id': {
                'N': '0'
            }
        },
        UpdateExpression="set r = :r, g = :g, b = :b",
        ExpressionAttributeValues = {
            ':r': {'N':r},
            ':g': {'N':g},
            ':b': {'N':b}
        }
    )
