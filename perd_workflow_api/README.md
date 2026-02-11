# `perd_workflow_api`

Public protocol package for PERD workflow microservices.

## Purpose

- Defines the canonical protobuf contract used by:
  - Workspace master service (Cloud Run) as gRPC client/proxy.
  - Workflow services (GKE pods) as gRPC servers.
- Gives contributors a stable API surface when forking `workflow/`.

## Package Layout

- `perd_workflow_api/v1/workflow.proto`: source-of-truth schema.
- `perd_workflow_api/v1/workflow_pb2.py`: protobuf message bindings.
- `perd_workflow_api/v1/workflow_pb2_grpc.py`: service bindings.
- `perd_workflow_api/client.py`: ergonomic Python client wrapper.

## Regenerating Bindings

If you update `workflow.proto`, regenerate bindings:

```bash
./scripts/generate_proto.sh
```

This requires `grpcio-tools` to be installed in the active environment.

## Example

```python
from perd_workflow_api import WorkflowClient

client = WorkflowClient("10.40.0.10:50051")
reply = client.add(2.5, 3.7, workflow_name="res-sim")
print(reply.result)
client.close()
```
