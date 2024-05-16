#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""vzdump-hook-script.pl ported to python

This is a port of vzdump-hook-script.pl (https://github.com/proxmox/pve-manager/blob/master/vzdump-hook-script.pl), with
lots of improvements.


Example parameters in production:

101: Sep 23 00:15:07 INFO: HOOK: backup-end snapshot 101
101: Sep 23 00:15:07 INFO: HOOK-ENV: vmtype=qemu;dumpdir=/dati1/dump;storeid=dati1;hostname=vmname;tarfile=/dati1/dump/vzdump-qemu-101-2016_09_22-23_10_01.vma.lzo;logfile=/dati1/dump/vzdump-qemu-101-2016_09_22-23_10_01.log
"""
import shlex
import sys
import os
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT, CalledProcessError, SubprocessError
import textwrap

import click
from dynaconf import ValidationError

from proxmox_grapple.vma_extractor import main as extractor
from .config import settings
from ._version import __version__



def dump_config(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    try:
        import dynaconf
        click.echo(dynaconf.inspect_settings(settings, print_report=True, dumper="yaml"))
    except ValidationError as e:
        print(e, file=sys.stderr)
    ctx.exit()


@click.command()
@click.option('--dump-config', is_flag=True, callback=dump_config, expose_value=False, is_eager=True,
              help='Dump config as determined by dynaconf')
@click.option('--config', '-c', required=False, help='Config file path')
@click.version_option(version=__version__)
@click.argument('phase')
@click.argument('mode', required=False)
@click.argument('vmid', required=False)
@click.pass_context
def main(ctx, config, phase, mode, vmid):
    """The grappling hook for Proxmox backups.  A more configurable replacement for the Perl version supplied by
    Proxmox Server Solutions GmbH.

    The required argument, PHASE, can be one of the following:

    job-init, job-start, job-end, job-abort, backup-start, backup-end,
    backup-abort, log-end, pre-stop, pre-restart, post-restart.  Anything
    else is ignored.
    """

    # Change dynaconf config file if specified
    if config:
        if Path(config).is_file():
            try:
                settings.load_file(path=config, silent=True, validate=True)
                click.echo(f'HOOK: Config file chosen: {config}')
            except ValidationError as e:
                click.echo(e, err=True)
                sys.exit(1)
        else:
            click.echo(f'ERROR: Config file does not exist: {config}', err=True)
            sys.exit(1)

    click.echo(f'HOOK: {" ".join(sys.argv)}')

    # if os.environ.get('STOREID', None) == 'pbs':
    #    click.echo('Detected running in Proxmox Backup Server, exiting')
    #    sys.exit(0)

    vmtype =  os.environ.get('VMTYPE') # openvz/qemu
    dumpdir = os.environ.get('DUMPDIR')
    storeid = os.environ.get('STOREID')
    hostname = os.environ.get('HOSTNAME')
    # tarfile is only available in phase 'backup-end'
    tarfile = os.environ.get('TARFILE')
    # logfile is only available in phase 'log-end'
    logfile = os.environ.get('LOGFILE')

    click.echo(f'HOOK-ENV: vmtype={vmtype}; dumpdir={dumpdir}; storeid={storeid}; hostname={hostname}; tarfile={tarfile}; logfile={logfile}')

    try:
        if settings.get(phase):
            try:
                if (settings[phase].extract.enabled and phase in ['backup-end']):
                    # example: copy resulting backup file to another host using scp, or use extractor()
                    if storeid != 'pbs':
                        click.echo(f'HOOK: {" ".join(sys.argv)}, running extractor', err=True)
                        # ctx.invoke(extractor, debug=False, name=tarfile)

            except KeyError:
                # Extraction not enabled
                pass

            if any(k in settings[phase] for k in ['script', 'shell']):
                mode = list(settings[phase].keys())[0]
                if mode == 'shell':
                    shell = True
                else:
                    shell = False

                for exec_line in settings[phase][mode]:
                    try:
                        click.echo(f'    Running (mode {mode}): {exec_line}')
                        if mode == 'script':
                            exec_line = shlex.split(exec_line)
                        with Popen(exec_line, stdout=PIPE, stderr=STDOUT, text=True, encoding='utf-8', shell=shell) as proc:
                            for line in proc.stdout:
                                click.echo(f'{textwrap.indent(line, " " * 4)}', nl=False)
                        rc = proc.returncode
                        if rc:
                            raise CalledProcessError(rc, exec_line)

                    except (CalledProcessError, SubprocessError, OSError) as e:
                        click.echo(f'{phase.upper()}: ERROR! Something went wrong', err=True)
                        click.echo(f'    {e}')

        else:
            click.echo(f'HOOK: Got unknown phase "{phase}", ignoring')

    except KeyError as e:
        click.echo(e, err=True)

    except ValidationError as e:
        click.echo(e, err=True)
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()
