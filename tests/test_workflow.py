"""Run these before you publish: `pip install "perd-worker[page]" pytest`, then `pytest`.

They check what the PERD build checks (the operations register and compile,
the page renders) and what your operations answer.
"""

import asyncio

import pytest
from perd_worker.compiler import compile_contract

import workflow


async def _stream(*values):
    for value in values:
        yield value


async def _collect(results):
    return [item async for item in results]


def test_the_operations_compile_as_on_perd():
    assert compile_contract("starter", workflow.workflow) is not None


def test_add():
    assert workflow.add(2.5, 3.7) == pytest.approx(6.2)


def test_total():
    assert asyncio.run(workflow.total(_stream(1.0, 2.0, 3.0), scale=2.0)) == pytest.approx(12.0)


def test_count_up():
    assert asyncio.run(_collect(workflow.count_up(0.0, 1.5, 3))) == [(0, 0.0), (1, 1.5), (2, 3.0)]


def test_running_mean():
    assert asyncio.run(_collect(workflow.running_mean(_stream(2.0, 4.0, 9.0)))) == [(1, 2.0), (2, 3.0), (3, 5.0)]


def test_the_page_renders():
    from perdlit._script import check_page

    summary = check_page("page", "workflow")
    assert summary
