"""Minimal local smoke test for workflow Add logic."""

from workflow import add

if __name__ == "__main__":
    result = add(2.5, 3.7)
    print(f"Result: {result}")  # Should print: 6.2
