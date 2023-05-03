from grpc_service import message_sender_pb2
from grpc_service import message_sender_pb2_grpc
from tasks.email import send_message_from_billing 


class MessageSender(message_sender_pb2_grpc.MessageSenderServicer):

    def SendBillingMessage(self, request, context):
        message_vars = {
            'role_description': request.role_description,
            'end_payment': request.end_payment
        }
        send_message_from_billing.delay(
            request.template_num,
            request.user_id,
            message_vars    
        )
        return message_sender_pb2.OperationResult(successful=True)