#!/usr/bin/env python3

from aws_cdk import core
from aws_cdk import aws_cognito as cognito
from aws_cdk import aws_dynamodb as ddb
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigateway as apigw



class ButtonCallStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define the Cognito User Pool
        user_pool = cognito.UserPool(self, 'ButtonAppUserPool',
            self_sign_up_enabled=True,
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            sign_in_aliases=cognito.SignInAliases(email=True),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True, mutable=True),
                phone_number=cognito.StandardAttribute(required=True, mutable=True)
            )
        )

        # Define the DynamoDB table to store user information
        users_table = ddb.Table(self, "UsersTable",
            partition_key=ddb.Attribute(
                name="userId",
                type=ddb.AttributeType.STRING
            ),
            removal_policy=core.RemovalPolicy.DESTROY  # This ensures the table is deleted when the stack is destroyed
        )

        # Lambda Function to handle call initiation logic
        call_initiation_lambda = _lambda.Function(self, "CallInitiationHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="call_initiation.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "USERS_TABLE": users_table.table_name
            }
        )

        # Grant the Lambda function permission to read from the DDB table
        users_table.grant_read_data(call_initiation_lambda)

        # API Gateway to trigger Lambda function
        api = apigw.LambdaRestApi(self, "Endpoint",
            handler=call_initiation_lambda
        )

app = core.App()
ButtonCallStack(app, "ButtonCallStack")
app.synth()
