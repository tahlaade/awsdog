#put path here
import boto3
from datadog import initialize, api
import time
import sys

# Get "Inctance ID" for all AWS instances, tagged as "production"


def get_aws_hostid(access_key_id, secret_access_key, region):
    inst = []
    session = boto3.Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        region_name=region
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

def get_dd_hostid(dd_api_key, dd_app_key):
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


def check_metric(awsinst, ddinst, environment):
    if len(awsinst) == len(ddinst):
        print 'All host in env:%s have dd metric' % environment
	return True
    else:
        print 'ALARM: Not all instance have metric'
        for i in awsinst:
            if not i in ddinst:
                print 'In host %s missing dd metric' % i
	return False

if __name__ == '__main__':
	try:
		access_key_id = sys.argv[1]
		secret_access_key = sys.argv[2]
		region_name = sys.argv[3]
		environment = sys.argv[4]
		dd_api_key = sys.argv[5]
		dd_app_key = sys.argv[6]
	except IndexError as e:
		print 'Some variables are not defined in cli \nsys.error:%s\n' % e

	now = int(time.time())
	print "\n"
	awsinst = get_aws_hostid(access_key_id, secret_access_key, region_name)
	print 'Count all aws-host in env:%s\t - %s' % (environment, len(awsinst))
	ddinst = get_dd_hostid(dd_api_key, dd_app_key)
	print 'Count all dd-host in env:%s\t - %s' % (environment, len(ddinst))
	print "\n"

	check_metric(awsinst, ddinst, environment)

	raw_input('Press enter to continue ...')
