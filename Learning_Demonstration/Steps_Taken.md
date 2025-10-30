# 1. Directory Structure

Using the terminal created: 

``` bash
Learning_Demonstration
├── greeting_ip_function
│   ├── app.py
│   └── requirements.txt
├── samconfig.toml
├── Steps_Taken.md
└── template.yaml

```

# 2. Integration of AWS Powertools Tutorial 

Modified to have a different naming convention for URL routing, python lambda function etc. 

### template.yaml

``` yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31
Description: Learning Demonstration using powertools


Globals:
  Function:
    Timeout: 3 
  Api:
    TracingEnabled: true


Resources:
  GreetingFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: greeting_ip_function/ 
      Handler: app.lambda_handler 
      Runtime: python3.13 
      Tracing: Active
      Architectures: 
        - x86_64
      Events:
        # Endpoint for GET /greeting
        GreetingNoName:
          Type: Api
          Properties:
            Path: /greeting
            Method: get
        # Endpoint for GET /greeting/{name}
        GreetingWithName:
          Type: Api
          Properties:
            Path: /greeting/{name} 
            Method: get
      Policies:
        - CloudWatchPutMetricPolicy: {}

Outputs:
  GreetingApi:
    Description: "API Gateway endpoint URL for Prod stage for greeting_ip_function (/greeting)"
    
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/greeting/"

  # Added an output for the new endpoint
  GreetingNameApi:
    Description: "API Gateway endpoint URL for Prod stage for greeting_ip_function (/greeting/{name})"
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/greeting/{name}"

```

 ### greeting_ip_function/app.py

 ``` python 
 from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.metrics import MetricUnit

logger = Logger(service="APP")
# Initialize tracer, define service name
tracer = Tracer(service="APP")
# initialize Metrics with our service name (APP) and metrics namespace (MyApp),
metrics = Metrics(namespace="MyApp", service="APP")
app = APIGatewayRestResolver()


@app.get("/greeting/<name>")
# @tracer.capture_method decorator
@tracer.capture_method
def greeting_name(name):
    logger.info(f"Request from {name} received")
    # Sends a data point with value 1 to CloudWatch - CloudWatch aggregates
    metrics.add_metric(name="SuccessfulGreetings", unit=MetricUnit.Count, value=1)
    return {"message": f"hello {name}!"}


@app.get("/greeting")
# @tracer.capture_method decorator
@tracer.capture_method
def greeting():
# tracer annotation to use value unknown during trace of /greeting route
    tracer.put_annotation(key="User", value="unknown")
    logger.info("Request from unknown received")
    # Sends a data point with value 1 to CloudWatch - CloudWatch aggregates
    metrics.add_metric(name="SuccessfulGreetings", unit=MetricUnit.Count, value=1)
    return {"message": "hello unknown!"}


@tracer.capture_lambda_handler
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event, context):
    try:
        return app.resolve(event, context)
    except Exception as e:
        logger.exception(e)
        raise

```

### greetinhg_ip_function/requirements.txt

``` text
aws-lambda-powertools
```

# Build and Test Locally

``` bash
sam build --use-container
```

![](screenshots/2025-10-30-19-37-26.png)

Start the local API:

``` bash
sam local start-api
```

![](screenshots/2025-10-30-19-40-57.png)

Using a new terminal: 

``` bash
# Test without name
curl http://localhost:3000/greeting

# Test with name  
curl http://localhost:3000/greeting/Ronan
```