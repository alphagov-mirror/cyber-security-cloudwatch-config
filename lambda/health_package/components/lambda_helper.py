""" SQS component helper functions """
import json

import botocore
from addict import Dict

from components.generic_helper import GenericHelper


class LambdaHelper(GenericHelper):
    """ Helper functions for Lambda """

    @classmethod
    def metric_resource_exists(cls, metric):
        """
        Check the resource exists before defining an alarm
        aws cloudwatch list-metrics returns metrics for resources that
        no longer exists
        """
        region = cls.get_metric_region(metric)
        namespace = metric.Namespace
        resource_exists = True
        try:
            print(f"Getting boto client for {namespace} in {region}")
            client = cls.get_client_from_namespace(namespace, region)
            if client:
                function_name = cls.get_metric_dimension_value(metric, "FunctionName")
                if function_name:
                    print(f"Get tags for lambda function: {function_name}")
                    client.get_function(FunctionName=function_name)
                else:
                    resource_exists = False

        except AttributeError as err:
            print(json.dumps(metric, indent=2))
            print(str(err))
        except botocore.exceptions.ClientError as err:
            print(str(err))
            resource_exists = False
        return resource_exists

    @classmethod
    def get_tags_for_metric_resource(cls, metric):
        """
        Get QueueUrl from queue name and then get the tags if present
        There is some duplication of the above function it would be nice to remove
        """
        region = cls.get_metric_region(metric)
        namespace = metric.Namespace
        tags = {}
        try:
            print(f"Getting boto client for {namespace} in {region}")
            client = cls.get_client_from_namespace(namespace, region)
            if client:
                function_name = cls.get_metric_dimension_value(metric, "FunctionName")
                if function_name:
                    print(f"Get tags for lambda function: {function_name}")
                    get_function_response = Dict(
                        client.get_function(FunctionName=function_name)
                    )
                    lambda_arn = get_function_response.Configuration.FunctionArn
                    get_tags_response = Dict(client.list_tags(Resource=lambda_arn))
                    tags = get_tags_response.Tags

        except AttributeError as err:
            print(json.dumps(metric, indent=2))
            print(str(err))
        except botocore.exceptions.ClientError as err:
            print(str(err))
        return tags

    @classmethod
    def get_metric_threshold(cls, metric, rule):
        if metric.MetricName == "Duration":
            region = cls.get_metric_region(metric)
            # Calculate duration threshold here.

            # Get the lambda timeout
            namespace = metric.Namespace
            # Assign a timeout outside of the try block
            lambda_timeout = 60
            try:
                print(f"Getting boto client for {namespace} in {region}")
                client = cls.get_client_from_namespace(namespace, region)
                if client:
                    function_name = cls.get_metric_dimension_value(
                        metric, "FunctionName"
                    )
                    if function_name:
                        print(f"Get timeout for lambda function: {function_name}")
                        get_function_response = Dict(
                            client.get_function(FunctionName=function_name)
                        )
                        lambda_timeout = get_function_response.Configuration.Timeout
            except AttributeError as err:
                print(json.dumps(metric, indent=2))
                print(str(err))
            except botocore.exceptions.ClientError as err:
                print(str(err))

            print(f"Set lambda timeout to: {lambda_timeout}")
            # 90% of max timeout seconds in milliseconds
            rule.Maximum = lambda_timeout * 1000 * 0.9
            print(f"Maximum threshold set to {rule.Maximum}")

        threshold = super().get_metric_threshold(metric, rule)

        return threshold
