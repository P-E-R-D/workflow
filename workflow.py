"""Template workflow module.

Only functions decorated with:

`@workflow.unary`, 
`@workflow.client_stream`,
`@workflow.server_stream`, or 
`@workflow.bi_di`

are built and exposed in generated workspace code.
"""

from per_datasets import workflow

@workflow.unary
def subtract(a: float, b: float) -> float:
    """Subtract two numbers.

    Example:
        >>> subtract(2.5, 3.7)
        -1.2
    """
    return a - b