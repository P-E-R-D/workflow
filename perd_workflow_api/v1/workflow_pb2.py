"""Generated-like protobuf module for perd/workflow/v1/workflow.proto."""
# Code generated manually because grpcio-tools is unavailable in this environment.
# Do not edit directly unless the matching .proto changes.

from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()

_TYPE_DOUBLE = _descriptor_pb2.FieldDescriptorProto.TYPE_DOUBLE
_TYPE_STRING = _descriptor_pb2.FieldDescriptorProto.TYPE_STRING
_TYPE_BOOL = _descriptor_pb2.FieldDescriptorProto.TYPE_BOOL
_TYPE_MESSAGE = _descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE
_LABEL_OPTIONAL = _descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL


def _add_field(
    message: _descriptor_pb2.DescriptorProto,
    *,
    name: str,
    number: int,
    field_type: int,
    type_name: str = "",
    oneof_index: int | None = None,
) -> None:
    field = message.field.add()
    field.name = name
    field.number = number
    field.label = _LABEL_OPTIONAL
    field.type = field_type
    if type_name:
        field.type_name = type_name
    if oneof_index is not None:
        field.oneof_index = oneof_index


def _add_messages(file_proto: _descriptor_pb2.FileDescriptorProto) -> None:
    add_request = file_proto.message_type.add()
    add_request.name = "AddRequest"
    _add_field(add_request, name="a", number=1, field_type=_TYPE_DOUBLE)
    _add_field(add_request, name="b", number=2, field_type=_TYPE_DOUBLE)
    _add_field(add_request, name="request_id", number=3, field_type=_TYPE_STRING)
    _add_field(add_request, name="workflow_name", number=4, field_type=_TYPE_STRING)

    add_reply = file_proto.message_type.add()
    add_reply.name = "AddReply"
    _add_field(add_reply, name="result", number=1, field_type=_TYPE_DOUBLE)
    _add_field(add_reply, name="request_id", number=2, field_type=_TYPE_STRING)
    _add_field(add_reply, name="workflow_name", number=3, field_type=_TYPE_STRING)
    _add_field(add_reply, name="status_message", number=4, field_type=_TYPE_STRING)

    stream_start = file_proto.message_type.add()
    stream_start.name = "StreamStart"
    _add_field(stream_start, name="session_id", number=1, field_type=_TYPE_STRING)
    _add_field(stream_start, name="job_id", number=2, field_type=_TYPE_STRING)
    _add_field(stream_start, name="workflow_name", number=3, field_type=_TYPE_STRING)
    _add_field(stream_start, name="operation", number=4, field_type=_TYPE_STRING)
    _add_field(stream_start, name="params_json", number=5, field_type=_TYPE_STRING)

    stream_chunk = file_proto.message_type.add()
    stream_chunk.name = "StreamChunk"
    _add_field(stream_chunk, name="session_id", number=1, field_type=_TYPE_STRING)
    _add_field(stream_chunk, name="job_id", number=2, field_type=_TYPE_STRING)
    _add_field(stream_chunk, name="chunk_id", number=3, field_type=_TYPE_STRING)
    _add_field(stream_chunk, name="payload_json", number=4, field_type=_TYPE_STRING)
    _add_field(stream_chunk, name="is_final", number=5, field_type=_TYPE_BOOL)

    job_cancel = file_proto.message_type.add()
    job_cancel.name = "JobCancel"
    _add_field(job_cancel, name="session_id", number=1, field_type=_TYPE_STRING)
    _add_field(job_cancel, name="job_id", number=2, field_type=_TYPE_STRING)
    _add_field(job_cancel, name="reason", number=3, field_type=_TYPE_STRING)

    job_stream_request = file_proto.message_type.add()
    job_stream_request.name = "JobStreamRequest"
    job_stream_request.oneof_decl.add().name = "payload"
    _add_field(
        job_stream_request,
        name="start",
        number=1,
        field_type=_TYPE_MESSAGE,
        type_name=".perd.workflow.v1.StreamStart",
        oneof_index=0,
    )
    _add_field(
        job_stream_request,
        name="chunk",
        number=2,
        field_type=_TYPE_MESSAGE,
        type_name=".perd.workflow.v1.StreamChunk",
        oneof_index=0,
    )
    _add_field(
        job_stream_request,
        name="cancel",
        number=3,
        field_type=_TYPE_MESSAGE,
        type_name=".perd.workflow.v1.JobCancel",
        oneof_index=0,
    )

    job_progress = file_proto.message_type.add()
    job_progress.name = "JobProgress"
    _add_field(job_progress, name="session_id", number=1, field_type=_TYPE_STRING)
    _add_field(job_progress, name="job_id", number=2, field_type=_TYPE_STRING)
    _add_field(job_progress, name="progress_percent", number=3, field_type=_TYPE_DOUBLE)
    _add_field(job_progress, name="message", number=4, field_type=_TYPE_STRING)

    job_result = file_proto.message_type.add()
    job_result.name = "JobResult"
    _add_field(job_result, name="session_id", number=1, field_type=_TYPE_STRING)
    _add_field(job_result, name="job_id", number=2, field_type=_TYPE_STRING)
    _add_field(job_result, name="result_json", number=3, field_type=_TYPE_STRING)

    job_error = file_proto.message_type.add()
    job_error.name = "JobError"
    _add_field(job_error, name="session_id", number=1, field_type=_TYPE_STRING)
    _add_field(job_error, name="job_id", number=2, field_type=_TYPE_STRING)
    _add_field(job_error, name="code", number=3, field_type=_TYPE_STRING)
    _add_field(job_error, name="message", number=4, field_type=_TYPE_STRING)

    job_stream_response = file_proto.message_type.add()
    job_stream_response.name = "JobStreamResponse"
    job_stream_response.oneof_decl.add().name = "event"
    _add_field(
        job_stream_response,
        name="progress",
        number=1,
        field_type=_TYPE_MESSAGE,
        type_name=".perd.workflow.v1.JobProgress",
        oneof_index=0,
    )
    _add_field(
        job_stream_response,
        name="result",
        number=2,
        field_type=_TYPE_MESSAGE,
        type_name=".perd.workflow.v1.JobResult",
        oneof_index=0,
    )
    _add_field(
        job_stream_response,
        name="error",
        number=3,
        field_type=_TYPE_MESSAGE,
        type_name=".perd.workflow.v1.JobError",
        oneof_index=0,
    )


def _add_service(file_proto: _descriptor_pb2.FileDescriptorProto) -> None:
    service = file_proto.service.add()
    service.name = "WorkflowService"

    add_method = service.method.add()
    add_method.name = "Add"
    add_method.input_type = ".perd.workflow.v1.AddRequest"
    add_method.output_type = ".perd.workflow.v1.AddReply"

    stream_method = service.method.add()
    stream_method.name = "RunJobStream"
    stream_method.input_type = ".perd.workflow.v1.JobStreamRequest"
    stream_method.output_type = ".perd.workflow.v1.JobStreamResponse"
    stream_method.client_streaming = True
    stream_method.server_streaming = True


def _build_descriptor():
    file_proto = _descriptor_pb2.FileDescriptorProto()
    file_proto.name = "perd/workflow/v1/workflow.proto"
    file_proto.package = "perd.workflow.v1"
    file_proto.syntax = "proto3"

    _add_messages(file_proto)
    _add_service(file_proto)

    return _descriptor_pool.Default().AddSerializedFile(file_proto.SerializeToString())


DESCRIPTOR = _build_descriptor()

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "perd_workflow_api.v1.workflow_pb2", globals())

__all__ = [
    "AddRequest",
    "AddReply",
    "StreamStart",
    "StreamChunk",
    "JobCancel",
    "JobStreamRequest",
    "JobProgress",
    "JobResult",
    "JobError",
    "JobStreamResponse",
]
