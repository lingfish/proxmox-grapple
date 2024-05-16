from subprocess import SubprocessError

import pytest
from click.testing import CliRunner
from proxmox_grapple.vzdump_hook_script import main


@pytest.fixture()
def runner(request):
    yield CliRunner()

def test_script_success(runner):
    result = runner.invoke(main, args=['job-end'], catch_exceptions=False)
    assert result.exit_code == 0
    assert 'This is a test.' in result.output

def test_script_fails_with_missing_command(runner):
    result = runner.invoke(main, args=['job-start'], catch_exceptions=False)
    assert 'ERROR! Something went wrong' in result.output
    assert 'No such file or directory' in result.output
    assert result.exit_code == 0

def test_script_fails_with_return_code(runner):
    result = runner.invoke(main, args=['backup-start'], catch_exceptions=False)
    assert 'ERROR! Something went wrong' in result.output
    assert 'returned non-zero exit status' in result.output
    assert result.exit_code == 0

def test_script_unknown_phase(runner):
    result = runner.invoke(main, args=['an-unknown-phase'], catch_exceptions=False)
    assert 'Got unknown phase' in result.output
    assert result.exit_code == 0

def test_script_missing_cli_config(runner):
    result = runner.invoke(main, args=['--config', '/nonexistent_file.yaml', 'job-end'], catch_exceptions=False)
    assert 'ERROR: Config file does not exist' in result.output
    assert result.exit_code == 1

def test_shell_success(runner):
    result = runner.invoke(main, args=['backup-abort'], catch_exceptions=False)
    assert result.exit_code == 0
    assert 'Thzs zs a test' in result.output

def test_script_fails_looks_like_shell(runner):
    result = runner.invoke(main, args=['pre-restart'], catch_exceptions=False)
    assert 'This is a test | tr i z' in result.output
    assert result.exit_code == 0
