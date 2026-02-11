"""
Workflow module exposing the `add` workflow function.

This package provides a simple `add(a, b)` function used by the
gRPC workflow server entrypoint (`main.py`).
"""

from .workflow import add

__all__ = ['add']
