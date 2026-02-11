#!/usr/bin/env python3
"""gRPC server entrypoint for workflow services."""
import asyncio
import json
import logging
import os

import grpc
from dotenv import load_dotenv
from grpc_health.v1 import health, health_pb2, health_pb2_grpc

from perd_workflow_api.v1 import workflow_pb2, workflow_pb2_grpc
from workflow import add as add_workflow

load_dotenv()
logger = logging.getLogger(__name__)


class WorkflowService(workflow_pb2_grpc.WorkflowServiceServicer):
    """Workflow gRPC service implementation."""

    async def Add(self, request, context):
        result = add_workflow(request.a, request.b)
        return workflow_pb2.AddReply(
            result=result,
            request_id=request.request_id,
            workflow_name=request.workflow_name or os.getenv("WORKFLOW_NAME", ""),
            status_message="ok",
        )

    async def RunJobStream(self, request_iterator, context):
        session_id = ""
        job_id = ""
        workflow_name = os.getenv("WORKFLOW_NAME", "")
        operation = ""
        total_chunks = 0

        async for request in request_iterator:
            payload_type = request.WhichOneof("payload")
            if payload_type == "start":
                session_id = request.start.session_id
                job_id = request.start.job_id
                workflow_name = request.start.workflow_name or workflow_name
                operation = request.start.operation or "run"
                yield workflow_pb2.JobStreamResponse(
                    progress=workflow_pb2.JobProgress(
                        session_id=session_id,
                        job_id=job_id,
                        progress_percent=0.0,
                        message=f"started operation={operation}",
                    )
                )
                continue

            if payload_type == "cancel":
                yield workflow_pb2.JobStreamResponse(
                    error=workflow_pb2.JobError(
                        session_id=session_id or request.cancel.session_id,
                        job_id=job_id or request.cancel.job_id,
                        code="CANCELLED",
                        message=request.cancel.reason or "cancelled",
                    )
                )
                return

            if payload_type != "chunk":
                continue

            total_chunks += 1
            chunk = request.chunk
            progress_percent = min(99.0, float(total_chunks) * 10.0)
            yield workflow_pb2.JobStreamResponse(
                progress=workflow_pb2.JobProgress(
                    session_id=session_id or chunk.session_id,
                    job_id=job_id or chunk.job_id,
                    progress_percent=progress_percent,
                    message=f"received chunk={chunk.chunk_id or total_chunks}",
                )
            )

            if chunk.is_final:
                result_payload = {"status": "completed", "operation": operation, "chunks": total_chunks}
                if operation == "add":
                    try:
                        values = json.loads(chunk.payload_json or "{}")
                        result_payload["result"] = add_workflow(float(values["a"]), float(values["b"]))
                    except Exception as exc:
                        yield workflow_pb2.JobStreamResponse(
                            error=workflow_pb2.JobError(
                                session_id=session_id or chunk.session_id,
                                job_id=job_id or chunk.job_id,
                                code="BAD_INPUT",
                                message=f"Invalid add payload: {exc}",
                            )
                        )
                        return

                yield workflow_pb2.JobStreamResponse(
                    result=workflow_pb2.JobResult(
                        session_id=session_id or chunk.session_id,
                        job_id=job_id or chunk.job_id,
                        result_json=json.dumps(result_payload),
                    )
                )
                return


async def serve() -> None:
    """Run the gRPC service until process termination."""
    port = int(os.getenv("PORT", os.getenv("GRPC_PORT", "50051")))
    address = f"[::]:{port}"

    server = grpc.aio.server(
        options=[
            ("grpc.keepalive_time_ms", 30000),
            ("grpc.keepalive_timeout_ms", 10000),
            ("grpc.http2.max_pings_without_data", 0),
            ("grpc.keepalive_permit_without_calls", 1),
        ]
    )

    workflow_pb2_grpc.add_WorkflowServiceServicer_to_server(WorkflowService(), server)

    health_servicer = health.aio.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    health_servicer.set(
        "perd.workflow.v1.WorkflowService",
        health_pb2.HealthCheckResponse.SERVING,
    )
    health_servicer.set("", health_pb2.HealthCheckResponse.SERVING)

    server.add_insecure_port(address)
    await server.start()
    logger.warning("Workflow gRPC server listening on %s", address)
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    asyncio.run(serve())
