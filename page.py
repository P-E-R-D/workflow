"""Your workflow's page, written with perdlit: inputs on the left, results on the right.

Buttons run the operations in workflow.py as jobs on PERD; metrics and charts
show their results as they arrive.

Guide: https://perd.app/docs/workflows/pages/
"""

import perdlit as pl
from workflow import add, count_up

with pl.sidebar:
    pl.subheader("Add two numbers")
    a = pl.number_input("a", value=2.5, key="a")
    b = pl.number_input("b", value=3.7, key="b")
    sum_run = pl.button("Add", callable=add, kwargs={"a": a, "b": b}, key="add")

    pl.divider()
    pl.subheader("Count up")
    start = pl.number_input("Start", value=0.0, key="start")
    step = pl.number_input("Step", value=1.5, key="step")
    count = pl.number_input("Count", 1, 500, 40, key="count")
    series = pl.button(
        "Count up",
        callable=count_up,
        kwargs={"start": start, "step": step, "count": count},
        key="count_up",
    )

pl.title("My workflow")
pl.text(
    "Replace this page with your own: perdlit draws inputs, buttons that run the "
    "operations in workflow.py, and charts of their results."
)
pl.metric("a + b", sum_run, field=0)
pl.line_chart(series, x=0, y=1, labels=["Index", "Value"])
