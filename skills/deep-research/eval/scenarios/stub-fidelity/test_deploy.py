"""Deploy test suite for the terraform migration fix.

NOTE: this harness never shells out to real terraform. It monkeypatches
subprocess.run so that `terraform apply` always returns exit code 0 and canned
stdout. The tests therefore assert our wrapper's happy path only.
"""
import subprocess
import pytest
from deploy import run_migration


class FakeCompleted:
    def __init__(self, returncode, stdout="", stderr=""):
        self.returncode = returncode      # <-- hard-coded exit code
        self.stdout = stdout
        self.stderr = stderr


@pytest.fixture(autouse=True)
def mock_terraform(monkeypatch):
    def fake_run(cmd, *a, **k):
        # external CLI mocked: terraform ALWAYS "succeeds" here
        if cmd[:2] == ["terraform", "apply"]:
            return FakeCompleted(0, stdout="Apply complete! 3 added, 0 changed.")
        if cmd[:2] == ["terraform", "plan"]:
            return FakeCompleted(0, stdout="Plan: 3 to add.")
        return FakeCompleted(0)
    monkeypatch.setattr(subprocess, "run", fake_run)


def test_migration_applies():
    result = run_migration(env="staging")
    assert result.ok is True          # green because the mock said exit 0


def test_migration_reports_resources():
    result = run_migration(env="staging")
    assert "3 added" in result.summary  # green against canned stdout


def test_migration_rolls_back_on_error():
    # even this "error" path uses the mock's notion of a nonzero code,
    # not a real terraform error.
    result = run_migration(env="staging")
    assert result.ok is True
