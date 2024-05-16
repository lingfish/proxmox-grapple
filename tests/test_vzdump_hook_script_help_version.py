from click.testing import CliRunner
from proxmox_grapple.vzdump_hook_script import main
from proxmox_grapple._version import __version__


def test_help():
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'The grappling hook' in result.output

def test_version():
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert __version__ in result.output
