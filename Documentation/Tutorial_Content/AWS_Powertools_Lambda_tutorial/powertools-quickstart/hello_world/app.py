from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths

logger = Logger(service="APP")
# Initialize tracer, define service name
tracer = Tracer(service="APP")
app = APIGatewayRestResolver()


@app.get("/hello/<name>")
# @tracer.capture_method decorator
@tracer.capture_method
def hello_name(name):
    logger.info(f"Request from {name} received")
    return {"message": f"hello {name}!"}


@app.get("/hello")
# @tracer.capture_method decorator
@tracer.capture_method
def hello():
# tracer annotation to use value unknown during trace of /hello route
    tracer.put_annotation(key="User", value="unknown")
    logger.info("Request from unknown received")
    return {"message": "hello unknown!"}


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
# Adds ColdStart annotation within Tracer itself. 
# Also add a new Service annotation using the value of Tracer(service="APP") - easy filtering
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    return app.resolve(event, context)