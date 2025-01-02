#!/bin/sh
if [ -z "${AWS_LAMBDA_RUNTIME_API}" ]; then
  exec aws-lambda-rie python3.10 -m awslambdaric $@
else
  exec python3.10 -m awslambdaric $@
fi