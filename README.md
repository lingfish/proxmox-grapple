# Proxmox-grapple

The Python app that "hooks" into Proxmox.

This is a clone of [vzdump-hook-script.pl](https://github.com/proxmox/pve-manager/blob/master/vzdump-hook-script.pl) that is
written in Python, and that offers a lot more configurability.

Different phases of the `vzdump` backup can be hooked into, and things can be run.

The app also logs script output in realtime -- useful when using a long-running process (like `rclone` for example),
and you want to see progressive timestamping against its output.

>⚠️ **NOTE!** Version 2.0.0 introduces a breaking change to the config file format!  See below.

## Table of contents

<!-- TOC -->
* [Proxmox-grapple](#proxmox-grapple)
  * [Table of contents](#table-of-contents)
  * [Purpose and uses](#purpose-and-uses)
    * [Running binaries](#running-binaries)
    * [Running things via a shell](#running-things-via-a-shell)
  * [Installation](#installation)
  * [Configuration](#configuration)
    * [Overview](#overview)
    * [Location](#location)
    * [Configuration dump](#configuration-dump)
    * [Configuration environments](#configuration-environments)
    * [Breaking change in 2.0.0](#breaking-change-in-200)
      * [Before 2.0.0 format](#before-200-format)
      * [New format](#new-format)
  * [Supported versions](#supported-versions)
<!-- TOC -->


## Purpose and uses

### Running binaries
Having hooks into each part of `vzdump` backups is very useful, especially to detect failures (or success) of the
different backup phases.

For example, it can be used in concert
with [Healthchecks.io](https://healthchecks.io/), [Mailrise](https://github.com/YoRyan/mailrise)/[Apprise](https://github.com/caronc/apprise),
or other apps, to receive status notifications:

```yaml
production:
  job-start:
    mode: script
    run:
      - "curl -fsS -m 10 --retry 5 -o /dev/null https://your.healthchecks.server/ping/xxx/vzdump-backups/start"
  job-abort:
    mode: script
    run:
      - "curl -fsS -m 10 --retry 5 -o /dev/null https://your.healthchecks.server/ping/xxx/vzdump-backups/fail"
  backup-abort:
    mode: script
    run:
      - "curl -fsS -m 10 --retry 5 -o /dev/null https://your.healthchecks.server/ping/xxx/vzdump-backups/fail"
```

Maybe you'd like to offsite-sync your backups on job completion:

```yaml
  job-end:
    mode: script
    run:
      - "ssh some.host rclone sync --checkers 32 --transfers 16 --dscp cs1 --stats-log-level NOTICE --stats-unit=bits --stats=2m /mnt/pbs-backups remote.host:pbs-rsync"
      - "curl -fsS -m 10 --retry 5 -o /dev/null https://your.healthchecks.server/ping/xxx/vzdump-backups"
```

Or maybe as [@lloydbayley](https://github.com/lloydbayley) uses it, via `curl`:

> It actually changes the RGB lights in my rack when a backup happens so it's purely decorative but I like to automate things.

Anything that can be run on the CLI, you can use here.

### Running things via a shell

Instead of using `mode: script`, you can use `mode: shell`, and anything configured will be run through a shell. This is
directly equivalent to the `shell` argument to Python's [`subprocess.Popen`](https://docs.python.org/3/library/subprocess.html#subprocess.Popen).

What's the benefit here?  To quote the Python documentation:

> If shell is True, the specified command will be executed through the shell. This can be useful if you are using Python
> primarily for the enhanced control flow it offers over most system shells and still want convenient access to other
> shell features such as shell pipes, filename wildcards, environment variable expansion, and expansion of ~ to a user’s
> home directory.

The shell used is `/bin/sh`.

>⚠️ **WARNING!** Read Python's [Security Considerations](https://docs.python.org/3/library/subprocess.html#security-considerations) section before using `shell`!
> 

### Environment

`proxmox-grapple` will expose the `vzdump` parameters to the following environment variables:

* `GRAPPLE_PHASE`
* `GRAPPLE_MODE`
* `GRAPPLE_VMID`

And all arguments in one:

* `GRAPPLE_ALL_ARGS`

These can then be used in your config as you see fit.  Note you'll need to use `shell` mode, or use binaries that can
read/expand/interpolate environment variables for you.

An example:

```shell
GRAPPLE_PHASE=backup-start
GRAPPLE_MODE=stop
GRAPPLE_VMID=102
GRAPPLE_ALL_ARGS=backup-start stop 102
```

## Installation

The recommended way to install `proxmox-grapple` is to use [pipx](https://pipx.pypa.io/stable/).

After getting `pipx` installed, simply run:

```shell
username@proxmox:~$ pipx install proxmox-grapple
```

Please [don't use pip system-wide](https://docs.python.org/3.11/installing/index.html#installing-into-the-system-python-on-linux).

You can of course also install it using classic virtualenvs.

Once installed, you need to tell Proxmox (specifically `vzdump`) to use the app. Edit `/etc/vzdump.conf` and add or edit
the `script` setting:

```yaml
script: /home/username/.local/bin/proxmox-grapple
```

No other changes to the file is needed.

## Configuration

### Overview

`proxmox-grapple` is configured with a YAML-style file.  An example:

```yaml
production:
  job-end:
    mode: script
    run:
      - echo 'hi'
      - sleep 1
      - echo 'there'
      - echo 'This is a test.'

  backup-end:
    mode: script
    run:
    extract:
      enabled: false
      source_directory: /tmp
      destination_directory: /tmp
  #    exclude_storeids:

  job-abort:
    mode: shell
    run:
      - echo 'your strange command' | tee some_logfile.txt
```

Each top-level key should match the different `vzdump` phases.  The currently recognised phases are:

* `job-init`
* `job-start`
* `job-end`
* `job-abort`
* `backup-start`
* `backup-end`
* `backup-abort`
* `log-end`
* `pre-stop`
* `pre-restart`
* `post-restart`

All of these are optional, and if not configured, are ignored.

If they *are* configured, the accompanying sub-keys are required:

* `mode`
* `run`

>⚠️ The extract argument is currently not tested, and should be treated as a proof-of-concept only.
### Location

The default location for the configuration is `/etc/proxmox_grapple.yml`, or `proxmox_grapple.yml` in the current
working directory, but this can also be specified on the commandline.

If a non-absolute path is given, Dynaconf will iterate upwards: it will look at each parent up to the root of the
system. For each visited folder, it will also try looking inside a `/config` folder.

### Configuration dump

There is a mode, `--dump-config`, that reads all possible configuration and then prints it out for validation purposes.

### Configuration environments

It can also use different configuration settings based on arbitrary environment names (eg. `production`, `lab`, etc.) It
uses the [Dynaconf](https://www.dynaconf.com/) Python project for configuration, so using environment variables to
choose the environment and any other configuration option is possible.

>⚠️ The default environment is `production`

For example, to choose a different configuration environment, set the environment variable `ENV_FOR_DYNACONF=lab`:

```shell
root@proxmox:~# ENV_FOR_DYNACONF=lab proxmox-grapple --dump-config
```

### Breaking change in 2.0.0

To enable the use of the two run modes, I've decided to change the schema of the config file that needs to be updated.

#### Before 2.0.0 format

```yaml
production:
  backup-start:
    script:
      - echo hi
```

#### New format
```yaml
production:
  backup-start:
    mode: script
    run:
      - echo hi
```

## Supported versions

`proxmox-grapple` supports the following VE versions:

| VE version | Debian version | Python version | VE EoL  |
|------------|----------------|----------------|---------|
| 8          | 12 (Bookworm)  | 3.11           | TBA     |
| 7          | 11 (Bullseye)  | 3.9            | 2024-07 |
