# Workflow Template

This repository is intentionally minimal. It is a source template that
the deployment pipeline transforms at build time into a runnable gRPC
workflow service.

## Files in this template

- `workflow.py`: Your workflow functions exposed with @workflow.** decorators
- `requirements.txt`: Python dependencies for your workflow code
- `README.md`: Usage notes
- `LICENSE`

## Decorators used for gRPC exposure

Mark functions you wish to expose in your `workflow.py` with one of:

- `@workflow.unary`         = One request on response (e.g server ping)
- `@workflow.client_stream` = Many request chunks, one response (e.g file storage)
- `@workflow.server_stream` = One request, multiple response chunks (e.g file request)
- `@workflow.bi_di`         = Bi-directional streaming of req/res chunks (e.g stream analytics)

During deployment, the server discovers these decorators, generates a
`protobuf`file, builds gRPC wrappers, and packages this server into
container files, then builds/deploys the application to the PERD platform.
