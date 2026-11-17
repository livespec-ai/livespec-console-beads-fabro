"""The documentation-only CI acceptance script runs green end to end."""

from __future__ import annotations

from collections.abc import Callable
from types import ModuleType

import pytest


@pytest.fixture
def workflow(load_script: Callable[[str], ModuleType]) -> ModuleType:
    return load_script("docs_only_ci_workflow.py")


def test_main_reports_the_lane_fail_closed(
    load_script: Callable[[str], ModuleType], capsys: pytest.CaptureFixture[str]
) -> None:
    load_script("check-docs-only-ci.py").main()

    assert "classification and lane wiring are fail-closed" in capsys.readouterr().out


def test_workflow_job_ends_at_the_next_sibling_job(workflow: ModuleType) -> None:
    text = "jobs:\n  first:\n    steps: a\n  second:\n    steps: b\n"

    assert workflow.workflow_job(text, "first") == "    steps: a"


def test_workflow_job_runs_to_the_end_when_it_is_last(workflow: ModuleType) -> None:
    text = "jobs:\n  only:\n    steps: a\n"

    assert workflow.workflow_job(text, "only") == "    steps: a\n"


def test_workflow_job_asserts_when_the_job_is_missing(workflow: ModuleType) -> None:
    with pytest.raises(AssertionError, match="no ghost job"):
        workflow.workflow_job("jobs:\n  real:\n    steps: a\n", "ghost")


def test_inline_run_script_stops_at_the_first_dedented_line(workflow: ModuleType) -> None:
    block = "        run: |\n          echo one\n\n          echo two\n        next: key\n"

    assert workflow.inline_run_script(block) == "echo one\n\necho two"


def test_inline_run_script_may_end_with_the_block(workflow: ModuleType) -> None:
    block = "        run: |\n          echo one\n"

    assert workflow.inline_run_script(block) == "echo one"


def test_inline_run_script_asserts_without_a_run_marker(workflow: ModuleType) -> None:
    with pytest.raises(AssertionError, match="no inline run script"):
        workflow.inline_run_script("        name: x\n")


def test_inline_run_script_asserts_on_an_empty_script(workflow: ModuleType) -> None:
    with pytest.raises(AssertionError, match="is empty"):
        workflow.inline_run_script("        run: |\n        next: key\n")


def test_skip_lane_verifier_keeps_every_required_leg_running(
    load_script: Callable[[str], ModuleType],
) -> None:
    load_script("check-docs-only-ci.py").check_skip_lane_verifier()


def test_check_matrix_wiring_rejects_a_job_level_skip(workflow: ModuleType) -> None:
    job = "    if: ${{ needs.merge-group-guard.outputs.skip != 'true' }}\n    steps:\n"
    with pytest.raises(AssertionError, match="must not be skipped at job level"):
        workflow.assert_check_matrix_skips_at_step_level(job)


def test_check_matrix_wiring_rejects_a_docs_only_job_level_skip(workflow: ModuleType) -> None:
    job = "    if: ${{ needs.classify-changes.outputs.docs_only != 'true' }}\n    steps:\n"
    with pytest.raises(AssertionError, match="must not be skipped at job level"):
        workflow.assert_check_matrix_skips_at_step_level(job)


def test_check_matrix_wiring_rejects_a_step_missing_the_docs_only_guard(
    workflow: ModuleType,
) -> None:
    job = (
        "    if: ${{ !cancelled() }}\n    steps:\n"
        "      - name: Report the skips (x)\n        run: echo\n"
        "      - name: Checkout\n"
        "        if: ${{ needs.merge-group-guard.outputs.skip != 'true' }}\n"
        "        uses: actions/checkout@v4\n"
    )
    with pytest.raises(AssertionError, match="lacks the skip guard"):
        workflow.assert_check_matrix_skips_at_step_level(job)


def test_check_matrix_wiring_rejects_an_unguarded_step(workflow: ModuleType) -> None:
    job = (
        "    if: ${{ !cancelled() }}\n    steps:\n"
        "      - name: Report the skips (x)\n        run: echo\n"
        "      - name: Checkout\n        uses: actions/checkout@v4\n"
    )
    with pytest.raises(AssertionError, match="lacks the skip guard"):
        workflow.assert_check_matrix_skips_at_step_level(job)
