FROM python:2.7-alpine

ADD awsdog.py /tmp/ddcheck.py 

RUN pip install boto3
RUN pip install datadog

CMD python /tmp/ddcheck.py $aws_access_key_id $aws_secret_access_key $region_name $environment $dd_api_key $dd_app_key
