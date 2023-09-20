import aws_cdk as core
import aws_cdk.assertions as assertions

from button_call.button_call_stack import ButtonCallStack

# example tests. To run these tests, uncomment this file along with the example
# resource in button_call/button_call_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ButtonCallStack(app, "button-call")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
