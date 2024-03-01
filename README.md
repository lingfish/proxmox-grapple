# Proxmox-grapple

The Python app that "hooks" into Proxmox.

This is a clone of [vzdump-hook-script.pl](https://github.com/proxmox/pve-manager/blob/master/vzdump-hook-script.pl) that is
written in Python, and that offers a lot more configurability.

Different phases of the `vzdump` backup can be hooked into, and scripts can be run.


## Configuration

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

The default location for the configuration is `/etc/proxmox_grapple.yml`, but this can also be specified on the
commandline.

It can also use different configuration based on environments. It uses the [Dynaconf](https://www.dynaconf.com/) Python
project for configuration, so using environment variables to choose the environment and any other configuration option is possible.

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

> [!NOTE]
> The extract argument is currently not tested, and should be treated as a proof-of-concept only.


## Supported versions

`proxmox-grapple` supports the following VE versions:

| VE version | Debian version | Python version | VE EoL  |
|------------|----------------|----------------|---------|
| 8          | 12 (Bookworm)  | 3.11           | TBA     |
| 7          | 11 (Bullseye)  | 3.9            | 2024-07 |


## Installation

The recommended way to install `proxmox-grapple` is to use [pipx](https://pipx.pypa.io/stable/).
