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


