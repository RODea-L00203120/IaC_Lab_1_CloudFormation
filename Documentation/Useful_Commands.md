# Useful CLI Trouble Shooting Commands

## Validate Template
aws cloudformation validate-template --template-body {{Template}}

## Pipe Stack Events logs to textfile

aws cloudformation describe-stack-events --stack-name restapi-cloudformation > stack_events.txt