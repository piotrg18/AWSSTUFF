import json
import boto3
import datetime

client = boto3.client('ce','us-east-1')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):
    now = datetime.datetime.utcnow()
    days = 1
    if 'days' in event:
        days = json.loads(event['days'])
    start = (now - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
    end = now.strftime('%Y-%m-%d')
    kwargs = {}
    data = client.get_cost_and_usage(TimePeriod={'Start': start, 'End':  end}, 
            Granularity='DAILY', Metrics=['UnblendedCost'], 
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}], **kwargs)
    return respond(None, data['ResultsByTime'])