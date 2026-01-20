"""
PINN Workflow Module
"""

from .workflow import train

__all__ = ['train']

# Server entrypoint: `main.py` provides a Flask interface to `train`.
