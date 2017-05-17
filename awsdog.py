#!/home/sviat/imprivata/virt-env/bin/python
import boto3
from datadog import initialize, api
import time
import sys

try:
    aws_access_key_id = sys.argv[1]
    aws_secret_access_key = sys.argv[2]
    region_name = sys.argv[3]
    environment = sys.argv[4]
    dd_api_key = sys.argv[5]
    dd_app_key = sys.argv[6]
except IndexError as e:
    print 'Some variables are not defined in cli \nsys.error:%s\n' % e

now = int(time.time())

# Get "Inctance ID" for all AWS instances, tagged as "production"


def get_aws_hostid():
    inst = []
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    ec2 = session.resource('ec2')

    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Environment', 'Values': [environment]}])
    try:
        for instance in instances:
            inst.append(instance.instance_id)
    except:
        print 'Error from aws'
        sys.exit(1)

    return inst


# Get a dictionary, with all "hosts" in environment:"production" registered in Datadog

def get_dd_hostid():
    inst = []
    options = {
        'api_key': dd_api_key,
        'app_key': dd_app_key
    }
    initialize(**options)

    query = 'system.cpu.system{environment:%s}by{host}' % environment
    output = api.Metric.query(start=now - 300, end=now, query=query)
    try:
        for i in output["series"]:
            inst.append(str(i["scope"].split(':')[2]))
    except:
        print 'Error from datadog'
        sys.exit(1)

    return inst

awsinst = get_aws_hostid()
ddinst = get_dd_hostid()
print "\n"

print 'Count all aws-host in env:%s\t - %s' % (environment, len(awsinst))
print 'Count all dd-host in env:%s\t - %s' % (environment, len(ddinst))
print "\n"


def check_metric():
    if len(awsinst) == len(ddinst):
        print 'All host in env:%s have dd metric' % environment
    else:
        print 'ALARM: Not all instance have metric'
        for i in awsinst:
            if not i in ddinst:
                print 'In host %s missing dd metric' % i

check_metric()

raw_input('Press enter to continue ...')
