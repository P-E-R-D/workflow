"""Ergonomic Python client wrapper around WorkflowService gRPC."""
from __future__ import annotations

import grpc

from perd_workflow_api.v1 import workflow_pb2, workflow_pb2_grpc


class WorkflowClient:
    """Simple synchronous client for community workflow consumers."""

    def __init__(self, target: str):
        self._channel = grpc.insecure_channel(target)
        self._stub = workflow_pb2_grpc.WorkflowServiceStub(self._channel)

    def add(self, a: float, b: float, workflow_name: str = "", request_id: str = "") -> workflow_pb2.AddReply:
        """Call unary Add RPC."""
        request = workflow_pb2.AddRequest(
            a=float(a),
            b=float(b),
            request_id=request_id,
            workflow_name=workflow_name,
        )
        return self._stub.Add(request)

    def close(self) -> None:
        """Close the underlying channel."""
        self._channel.close()
