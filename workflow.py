"""Template workflow module.

Only functions decorated with:

`@workflow.unary`,
`@workflow.input_stream`,
`@workflow.output_stream`, or
`@workflow.bi_di`

are built and exposed in generated workspace code.
"""
from per_datasets import workflow
from per_datasets.workflow import WorkflowStreamInput, WorkflowStreamOutput


@workflow.unary
def add(a: float, b: float) -> float:
    """Add two numbers.

    Example:
        >>> add(2.5, 3.7)
        6.2
    """
    return a + b


@workflow.input_stream
async def sum_stream(inputStream: WorkflowStreamInput[float], max_iters: int) -> float:
    """Consume an input stream and return one aggregate result.

    Runtime usage:
        >>> pds_session.workflows("<deployment_id>").sum_stream([[1.0], [2.0], [3.0]], max_iters=3)
        6.0
    """
    total = 0.0
    index = 0
    async for value in inputStream:
        total += float(value)
        index += 1
        if index >= int(max_iters):
            break
    return total


@workflow.output_stream
def count_up(seed: float, step: float, count: int) -> WorkflowStreamOutput[float]:
    """Return a server-side stream from multi-parameter inputs.

    Runtime usage:
        >>> list(pds_session.workflows("<deployment_id>").count_up(seed=2.0, step=1.5, count=4))
        [2.0, 3.5, 5.0, 6.5]
    """
    start = float(seed)
    delta = float(step)
    size = max(0, int(count))
    return [start + (idx * delta) for idx in range(size)]


@workflow.bi_di
async def compute_nn_layer(inputStream: WorkflowStreamInput[float, int, bool]) -> WorkflowStreamOutput[float]:
    """Consume a bidirectional stream and yield transformed cumulative totals.

    Runtime usage:
        >>> list(pds_session.workflows("<deployment_id>").compute_nn_layer([
        ...     {"value": 3.0, "scale": 2.0, "bias": 1.0},
        ...     {"value": 5.0, "scale": 0.5, "bias": -0.5},
        ... ]))
        [7.0, 9.0]
        >>> list(pds_session.workflows("<deployment_id>").compute_nn_layer([
        ...     [3.0, 2.0, 1.0],
        ...     [5.0, 0.5, -0.5],
        ... ]))
        [7.0, 9.0]
        >>> list(pds_session.workflows("<deployment_id>").compute_nn_layer(<generator of [3.0, 2.0, 1.0] or {"value": 5.0, "scale": 0.5, "bias": -0.5}>))
        [7.0, 9.0]
    """
    total = 0.0
    async for value, scale, bias in inputStream:  # generated runtime passes an async input iterator
        current = float(value) * float(scale) + float(bias)
        total += current
        yield total
