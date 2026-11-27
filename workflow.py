"""Your workflow: the operations PERD builds, lists in the Store and serves.

Mark a function with one of the four decorators to expose it. Arguments and
results are scalars (float, int, str, bool, bytes); streams carry tuples of
scalars. Rename, replace and add operations freely: PERD reads them when it
builds your repository.

Guide: https://perd.app/docs/getting-started/first-workflow/
"""

from __future__ import annotations

from perd_worker import WorkflowStreamInput, WorkflowStreamOutput, workflow


@workflow.unary
def add(a: float, b: float) -> float:
    """Add two numbers: one call, one answer."""
    return a + b


@workflow.input_stream
async def total(values: WorkflowStreamInput[float], scale: float = 1.0) -> float:
    """Sum a stream of numbers sent one by one, then answer once, times ``scale``."""
    result = 0.0
    async for value in values:
        result += float(value)
    return result * scale


@workflow.output_stream
async def count_up(start: float, step: float, count: int) -> WorkflowStreamOutput[int, float]:
    """Answer with a stream of (index, value) pairs: ``start``, ``start + step``, and so on."""
    for index in range(int(count)):
        yield index, start + index * step


@workflow.bi_di
async def running_mean(values: WorkflowStreamInput[float]) -> WorkflowStreamOutput[int, float]:
    """Read a stream and answer as it goes: (values so far, their mean) after each one."""
    seen = 0
    total_so_far = 0.0
    async for value in values:
        seen += 1
        total_so_far += float(value)
        yield seen, total_so_far / seen
