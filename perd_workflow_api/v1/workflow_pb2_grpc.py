"""gRPC service bindings for perd.workflow.v1.WorkflowService."""

import grpc

from . import workflow_pb2 as workflow__pb2


class WorkflowServiceStub:
    """Client stub for WorkflowService."""

    def __init__(self, channel):
        self.Add = channel.unary_unary(
            "/perd.workflow.v1.WorkflowService/Add",
            request_serializer=workflow__pb2.AddRequest.SerializeToString,
            response_deserializer=workflow__pb2.AddReply.FromString,
        )
        self.RunJobStream = channel.stream_stream(
            "/perd.workflow.v1.WorkflowService/RunJobStream",
            request_serializer=workflow__pb2.JobStreamRequest.SerializeToString,
            response_deserializer=workflow__pb2.JobStreamResponse.FromString,
        )


class WorkflowServiceServicer:
    """Server-side interface for WorkflowService."""

    def Add(self, request, context):
        raise NotImplementedError("Method not implemented")

    def RunJobStream(self, request_iterator, context):
        raise NotImplementedError("Method not implemented")


def add_WorkflowServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "Add": grpc.unary_unary_rpc_method_handler(
            servicer.Add,
            request_deserializer=workflow__pb2.AddRequest.FromString,
            response_serializer=workflow__pb2.AddReply.SerializeToString,
        ),
        "RunJobStream": grpc.stream_stream_rpc_method_handler(
            servicer.RunJobStream,
            request_deserializer=workflow__pb2.JobStreamRequest.FromString,
            response_serializer=workflow__pb2.JobStreamResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "perd.workflow.v1.WorkflowService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


class WorkflowService:
    """Experimental static helpers matching protoc output style."""

    @staticmethod
    def Add(request, target, options=(), channel_credentials=None, call_credentials=None,
            insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/perd.workflow.v1.WorkflowService/Add",
            workflow__pb2.AddRequest.SerializeToString,
            workflow__pb2.AddReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def RunJobStream(request_iterator, target, options=(), channel_credentials=None, call_credentials=None,
                     insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            "/perd.workflow.v1.WorkflowService/RunJobStream",
            workflow__pb2.JobStreamRequest.SerializeToString,
            workflow__pb2.JobStreamResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
