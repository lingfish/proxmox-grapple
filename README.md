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