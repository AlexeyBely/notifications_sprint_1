import grpc
import logging
from concurrent import futures

from grpc_service.message_sender_server import MessageSender
from grpc_service import message_sender_pb2_grpc
from core.config import settings


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    message_sender_pb2_grpc.add_MessageSenderServicer_to_server(
        MessageSender(), server)
    server.add_insecure_port(f'[::]:{settings.notify_grpc_port}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()