# Tutorial Follow along steps
Available at: https://docs.aws.amazon.com/powertools/python/latest/tutorial/#requirements

## Initialize project from template using SAM tool

sam init --runtime python3.13 --dependency-manager pip --app-template hello-world --name powertools-quickstart

![](screenshots/2025-10-22-11-02-49.png)

This results in the following project structure: 

```
`-- powertools-quickstart
    |-- events
    |   `-- event.json
    |-- hello_world
    |   |-- app.py
    |   |-- __init__.py
    |   `-- requirements.txt
    |-- __init__.py
    |-- README.md
    |-- samconfig.toml
    |-- template.yaml
    `-- tests
        |-- __init__.py
        |-- integration
        |   |-- __init__.py
        |   `-- test_api_gateway.py
        |-- requirements.txt
        `-- unit
            |-- __init__.py
            `-- test_handler.py
```

## Files in focus:

app.py - Application code.

template.yaml - AWS infrastructure configuration using SAM.

requirements.txt - List of extra Python packages needed.

## Modify app.py:
``` python
import json


def hello():
    return {"statusCode": 200, "body": json.dumps({"message": "hello unknown!"})}


def lambda_handler(event, context):
    return hello()

```

## Modify template.yaml

``` yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Sample SAM Template for powertools-quickstart
Globals:
    Function:
        Timeout: 3
Resources:
    HelloWorldFunction:
        Type: AWS::Serverless::Function
        Properties:
            CodeUri: hello_world/
            Handler: app.lambda_handler
            Runtime: python3.13
            Architectures:
                - x86_64
            Events:
                HelloWorld:
                    Type: Api
                    Properties:
                        Path: /hello
                        Method: get
Outputs:
    HelloWorldApi:
        Description: "API Gateway endpoint URL for Prod stage for Hello World function"
        Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/hello/" 
```

## Run Code locally using SAM: 

Without a container you are required to have the python 3.13 on your path; I didn't so I went with a container solution. 

``` bash
sam build && sam local start-api
```

## Run using a docker container: 

``` bash
sam build --use-container && sam local start-api
```

![](screenshots/2025-10-22-11-44-07.png)

![](screenshots/2025-10-22-11-45-37.png)

## Invoke function: 

``` bash 
curl http://127.0.0.1:3000/hello 
```

![](screenshots/2025-10-22-17-26-44.png)


