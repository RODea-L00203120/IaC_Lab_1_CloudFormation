### **Manual Deployment Using the AWS Console**

This method involves creating and configuring resources directly through the AWS web interface. The REST API will consist of a **Lambda function** that handles the logic and an **API Gateway** that acts as the public endpoint.

#### **Creating the API Gateway**

1.  Navigate to **API Gateway** in the AWS Console.
2.  Choose **Create API**, select the **REST API** option, and click **Build**.
3.  Choose **New API**, provide a name such as `whats-my-ip`, and click **Create API**.

#### **Creating the API Resource and Method**

1.  From the **Actions** menu, select **Create Resource**. Set the **Resource Name** and **Resource Path** to `ip`.
2.  With the newly created resource selected, go to **Actions** and select **Create Method**.
3.  Choose **GET** from the dropdown menu and click the checkmark to save.

#### **Creating the Lambda Function**

1.  Go to the **Lambda** service in the AWS Console.
2.  Click **Create function**, choose the **Python 3.9** runtime, and give the function a descriptive name like `get_ip`.
3.  In the code editor, replace the default code with the following Python script. This code gets the IP address from the incoming request and returns it in a JSON format.
    ```python
    import json

    def lambda_handler(event, context):
        ip_address = event['requestContext']['identity']['sourceIp']
        return {
            'statusCode': 200,
            'body': json.dumps({"ip_address": ip_address}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    ```
4.  Click **Deploy** to save the changes.

#### **Integrating and Deploying the API**

1.  Return to the API Gateway console and select the **GET** method you created.
2.  For **Integration type**, choose **Lambda Function**.
3.  Check the box for **Use Lambda Proxy integration**.
4.  For **Lambda Function**, start typing the name of your function (`get_ip`) and select it from the list.
5.  Click **Save**.
6.  To make the API publicly accessible, go to the **Actions** menu and select **Deploy API**.
7.  Create a **New Stage**, name it `dev`, and click **Deploy**.

-----

### **Scripted Deployment Using CloudFormation**

This method uses **Infrastructure as a Code** to define all resources in a single YAML template. This approach is more efficient for repeatability and version control.

#### **The CloudFormation Template**

The following YAML template defines all the necessary components for the API, including the Lambda function, API Gateway, and the required IAM roles.

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: REST API using AWS API Gateway with a Lambda Integration
Resources:
  SimpleRestAPI:
    Type: AWS::ApiGateway::RestApi
    Properties:
      Description: REST API that gets users IP
      EndpointConfiguration:
        Types:
          - REGIONAL
      Name: whats-my-ip-cf
  ApiGatewayResource:
    Type: AWS::ApiGateway::Resource
    Properties:
      ParentId: !GetAtt SimpleRestAPI.RootResourceId
      PathPart: "ip_v2"
      RestApiId: !Ref SimpleRestAPI
  ApiGatewayMethod:
    Type: AWS::ApiGateway::Method
    Properties:
      HttpMethod: GET
      AuthorizationType: NONE
      Integration:
        Credentials: !GetAtt ApiGatewayIamRole.Arn
        IntegrationHttpMethod: POST
        Type: AWS_PROXY
        Uri: !Sub "arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${LambdaFunction.Arn}/invocations"
      ResourceId: !Ref ApiGatewayResource
      RestApiId: !Ref SimpleRestAPI
  ApiGatewayModel:
    Type: AWS::ApiGateway::Model
    Properties:
      ContentType: "application/json"
      RestApiId: !Ref SimpleRestAPI
      Schema: {}
  ApiGatewayStage:
    Type: AWS::ApiGateway::Stage
    Properties:
      DeploymentId: !Ref ApiGatewayDeployment
      Description: REST API dev stage
      RestApiId: !Ref SimpleRestAPI
      StageName: "dev"
  ApiGatewayDeployment:
    Type: AWS::ApiGateway::Deployment
    DependsOn: ApiGatewayMethod
    Properties:
      Description: Lambda API Deployment
      RestApiId: !Ref SimpleRestAPI
  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      Code:
        ZipFile: |
          import json
          def lambda_handler(event, context):
              ip_address = event['requestContext']['identity']['sourceIp']
              return {
                  'body': json.dumps({"ip_address": ip_address}),
                  'headers': {
                      'Content-Type': 'application/json'
                  },
                  'statusCode': 200
              }
      Description: AWS Lambda function
      FunctionName: "get_ip_v2"
      Handler: index.lambda_handler
      MemorySize: 256
      Role: !GetAtt LambdaIamRole.Arn
      Runtime: python3.9
      Timeout: 60
  ApiGatewayIamRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Sid: ""
            Effect: "Allow"
            Principal:
              Service:
                - "apigateway.amazonaws.com"
            Action:
              - "sts:AssumeRole"
      Path: "/"
      Policies:
        - PolicyName: LambdaAccessPolicy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: "Allow"
                Action: "lambda:*"
                Resource: !GetAtt LambdaFunction.Arn
  LambdaIamRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: "Allow"
            Principal:
              Service:
                - "lambda.amazonaws.com"
            Action:
              - "sts:AssumeRole"
      Path: "/"
```

#### **Deploying the Template with the AWS CLI**

After saving the template as `template.yaml`, use the AWS CLI to deploy it. It is recommended to validate the template first to catch syntax errors.

1.  **Validate the template**:

    ```bash
    aws cloudformation validate-template --template-body file://template.yaml
    ```

    This command checks the template for syntax and logical errors before deployment.

2.  **Deploy the API**:

    ```bash
    aws cloudformation deploy --template-file template.yaml --stack-name restapi-cloudformation --capabilities CAPABILITY_IAM
    ```

    The `CAPABILITY_IAM` flag is necessary because the template creates IAM roles.

-----

### **Troubleshooting with CloudFormation Logs**

The initial deployment failed because a Lambda function named **`get_ip`** already existed in the AWS account, causing a naming conflict. This issue was diagnosed by piping the CloudFormation stack events to a text file.

By running the command `aws cloudformation describe-stack-events --stack-name restapi-cloudformation > stack_events.txt`, a log file was created. An analysis of this file showed a `CREATE_FAILED` event for the `LambdaFunction` resource, with the explicit reason: "Function creation failed because the function already exists". Updating the CloudFormation template to use a unique name for both the Lambda function (`get_ip_v2`) and the API Gateway resource path (`ip_v2`) rectified this.