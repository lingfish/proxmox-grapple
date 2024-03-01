# Proxmox-grapple

The Python app that "hooks" into Proxmox.

This is a clone of [vzdump-hook-script.pl](https://github.com/proxmox/pve-manager/blob/master/vzdump-hook-script.pl) that is
written in Python, and that offers a lot more configurability.

Different phases of the `vzdump` backup can be hooked into, and scripts can be run.

## Configuration

`proxmox-grapple` is configured with a YAML-style file.  An example:

```yaml
job-end:
  script:
    - echo 'hi'
    - sleep 1
    - echo 'there'

backup-end:
  extract: true
```

## Supported versions

`proxmox-grapple` supports the following VE versions:

| VE version | Debian version | Python version | VE EoL  |
|------------|----------------|----------------|---------|
| 8          | 12 (Bookworm)  | 3.11           | TBA     |
| 7          | 11 (Bullseye)  | 3.9            | 2024-07 |


## Installation

The recommended way to install `proxmox-grapple` is to use [pipx](https://pipx.pypa.io/stable/).
