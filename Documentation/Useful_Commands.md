# Useful CLI Trouble Shooting Commands

## Validate Template
aws cloudformation validate-template --template-body {{Template}}

## Pipe Stack Events logs to textfile

aws cloudformation describe-stack-events --stack-name restapi-cloudformation > stack_events.txt

## Upload template & deploy API (formatted for powershell)

aws cloudformation deploy `
  --template template.yaml `
  --stack-name restapi-cloudformation `
  --capabilities CAPABILITY_IAM

## Useful/Core docker commands

## Build 
docker buildx build --platform linux/amd64 --provenance=false -t docker-image:test

## Run, maps local port 9000 to the container's port 8080
docker run -p 9000:8080 docker-image:test

## Stop a running container
First, find the CONTAINER ID of your running container:

docker ps

Then, use that ID to stop (kill) it:

docker kill <CONTAINER ID>