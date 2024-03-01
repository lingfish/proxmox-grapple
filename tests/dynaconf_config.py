from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=['tests/proxmox_grapple_tests.yml'],
    environments=True,
)