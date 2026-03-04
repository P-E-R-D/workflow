"""Template workflow module.

Only functions decorated with:

`@workflow.unary`, 
`@workflow.client_stream`,
`@workflow.server_stream`, or 
`@workflow.bi_di`

are built and exposed in generated workspace code.
"""
from typing import AsyncGenerator

from per_datasets import workflow


@workflow.unary
def add(a: float, b: float) -> float:
    """Add two numbers.

    Example:
        >>> pds_session.workflows("<deployment_id>").add(2.5, 3.7)
        6.2
    """
    return a + b

# TODO: Use slightly more complex examples with multi-parameter inputs for each type of workflow function below.
@workflow.client_stream
def sum_stream(value: float) -> float:
    """Sum a streamed list of numbers from the client.

    Runtime usage:
        >>> pds_session.workflows("<deployment_id>").sum_stream([1.0, 2.0, 3.0])
        6.0
    """
    if isinstance(value, list):
        return float(sum(value))
    return float(value)


@workflow.server_stream
def count_up(seed: float) -> list[float]:
    """Return a small server-side stream derived from one input.

    Runtime usage:
        >>> list(pds_session.workflows("<deployment_id>").count_up(2.0))
        [2.0, 3.0, 4.0]
    """
    start = float(seed)
    return [start, start + 1.0, start + 2.0]


@workflow.bi_di
async def running_total(value: float) -> AsyncGenerator[float, None]:
    """Consume a bidirectional input stream and yield cumulative totals.

    Runtime usage:
        >>> list(pds_session.workflows("<deployment_id>").running_total([1.0, 2.0, 3.0]))
        [1.0, 3.0, 6.0]
    """
    total = 0.0
    async for item in value:  # generated runtime passes an async input iterator
        if isinstance(item, dict):
            item = item.get("value", 0.0)
        total += float(item)
        yield total
