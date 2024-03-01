#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is code that implements a VMA extractor.

It's a little messy, and is mostly a proof of concept.
"""

import os
import logging
import psutil
from subprocess import Popen, PIPE
import re
import datetime

import click
import daiquiri
import humanize


logger = daiquiri.getLogger(__name__)

def process(debug, name):
    if debug:
        log_formatter = daiquiri.formatter.ColorFormatter(
            fmt='%(asctime)s %(levelname)s %(name)s %(color)s%(message)s%(color_stop)s')
        log_level = logging.DEBUG
    else:
        log_formatter = daiquiri.formatter.ColorFormatter(
            fmt='%(asctime)s %(levelname)s %(color)s%(message)s%(color_stop)s')
        log_level = logging.INFO

    outputs = daiquiri.output.Stream(level=log_level, formatter=log_formatter)
    daiquiri.setup(level=log_level, outputs=[outputs])

    logger.info('Starting vma_extractor')
    logger.info('Name pattern: %s', name)
    for file in os.scandir('/mnt/pve/nas_VMs/dump'):
        logger.debug('Filename: %s', file.name)
        if name in file.name or name == file.path:
            if file.name.startswith('vzdump-qemu'):
                if file.name.endswith('lzo'):
                    basename = os.path.splitext(os.path.splitext(file.name)[0])[0]
                    logger.info('Found a lzo, basename: %s, size %s', basename, humanize.naturalsize(file.stat().st_size))

                    dest = '/mnt/nas/vma/' + basename

                    if os.path.exists(dest):
                        logger.info('Extraction path %s exists, skipping', dest)
                        continue

                    lzop = psutil.Popen(['lzop', '-dc', file.path], stdout=PIPE)
                    vma = psutil.Popen(['vma', 'extract', '-v', '-', '/mnt/nas/vma/' + basename], stdin=lzop.stdout, stdout=PIPE)
                    lzop.ionice(psutil.IOPRIO_CLASS_BE, value=7)
                    vma.ionice(psutil.IOPRIO_CLASS_BE, value=7)
                    logger.info('Starting extraction of %s to %s', file.path, dest)
                    with click.progressbar(length=100,
                                           label='Extracting {}'.format(file.name)) as bar:
                        percent = 0
                        current_percent = 0
                        while True:
                            output = vma.stdout.readline()
                            if output == b'' and vma.poll() is not None:
                                logger.debug('out')
                                break
                            if output:
                                logger.debug('output "%s", percent: %i, current: %i', output.decode('utf-8').strip(), percent, current_percent)
                                r = re.match(rb'progress ([^ %]+)%', output)
                                if r:
                                    if r.group(1):
                                        current_percent = int(r.group(1).decode('utf-8'))
                                        step = current_percent - percent
                                        bar.update(step)
                                        percent = current_percent

                    logger.debug('about to poll')
                    rc = vma.poll()
                    logger.info('Finished extraction of %s to %s', file.path, dest)

@click.command()
@click.option('--debug', '-d', is_flag=True, default=False, help='Turn on debugging')
@click.option('--name', '-n', required=True, default=datetime.datetime.now().strftime("%Y_%m_%d"), help='Subset of archive name to extract')
def main(debug, name):
    process(debug, name)


if __name__ == '__main__':
    main()
