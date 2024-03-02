# Proxmox-grapple

The Python app that "hooks" into Proxmox.

This is a clone of [vzdump-hook-script.pl](https://github.com/proxmox/pve-manager/blob/master/vzdump-hook-script.pl) that is
written in Python, and that offers a lot more configurability.

Different phases of the `vzdump` backup can be hooked into, and scripts can be run.

<!-- TOC -->
* [Proxmox-grapple](#proxmox-grapple)
  * [Installation](#installation)
  * [Configuration](#configuration)
    * [Overview](#overview)
    * [Location](#location)
    * [Configuration environments](#configuration-environments)
  * [Supported versions](#supported-versions)
<!-- TOC -->

## Installation

The recommended way to install `proxmox-grapple` is to use [pipx](https://pipx.pypa.io/stable/).

After getting `pipx` installed, simply run:

```shell
username@proxmox:~$ pipx install proxmox-grapple
```

Please, please [don't use pip system-wide](https://docs.python.org/3.11/installing/index.html#installing-into-the-system-python-on-linux).

Once installed, you need to tell Proxmox (specifically `vzdump`) to use the app. Edit `/etc/vzdump.conf` and add or edit
the `script` setting:

```yaml
script: /home/username/.local/bin/proxmox-grapple
```


## Configuration

### Overview

`proxmox-grapple` is configured with a YAML-style file.  An example:

```yaml
production:
  job-end:
    script:
      - echo 'hi'
      - sleep 1
      - echo 'there'
      - echo 'This is a test.'

  backup-end:
    extract:
      enabled: false
      source_directory: /tmp
      destination_directory: /tmp
  #    exclude_storeids:
```

### Location

The default location for the configuration is `/etc/proxmox_grapple.yml`, or `proxmox_grapple.yml` in the current
working directory, but this can also be specified on the commandline.

If a non-absolute path is given, Dynaconf will iterate upwards: it will look at each parent up to the root of the
system. For each visited folder, it will also try looking inside a `/config` folder.

### Configuration environments

It can also use different configuration settings based on arbitrary environment names (eg. `production`, `lab`, etc.) It
uses the [Dynaconf](https://www.dynaconf.com/) Python project for configuration, so using environment variables to
choose the environment and any other configuration option is possible.

>⚠️ The default environment is `production`

For example, to choose a different configuration environment, set the environment variable `ENV_FOR_DYNACONF=lab`:

```shell
root@proxmox:~# ENV_FOR_DYNACONF=lab proxmox-grapple --dump-config
```
Each top-level key should match the different `vzdump` phases.  The currently recognised phases are:

* job-init
* job-start
* job-end
* job-abort
* backup-start
* backup-end
* backup-abort
* log-end
* pre-stop
* pre-restart
* post-restart

>⚠️ The extract argument is currently not tested, and should be treated as a proof-of-concept only.


## Supported versions

`proxmox-grapple` supports the following VE versions:

| VE version | Debian version | Python version | VE EoL  |
|------------|----------------|----------------|---------|
| 8          | 12 (Bookworm)  | 3.11           | TBA     |
| 7          | 11 (Bullseye)  | 3.9            | 2024-07 |
