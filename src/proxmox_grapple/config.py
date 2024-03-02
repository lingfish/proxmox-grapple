from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    settings_files=['proxmox_grapple.yml', '/etc/proxmox_grapple.yml'],
    environments=True,
    env='production',
    apply_default_on_none=True,
    core_loaders=['YAML'],
    validators=[
        Validator('job-init', 'job-start', 'job-end', 'job-abort', 'backup-start', 'backup-end', 'backup-abort',
                  'log-end', 'pre-stop', 'pre-restart', 'post-restart', default={'script': None}
                  ),
        Validator(
            'backup-end.extract.enabled',
            default=False
        ),
        Validator(
            'backup-end.extract.enabled',
            must_exist=True,
            when=Validator("backup-end.extract", must_exist=True),
            messages={'must_exist_true': 'ERROR: {name} is required when extract is configured'}
        ),
        Validator(
            'backup-end.extract.source_directory',
            'backup-end.extract.destination_directory',
            must_exist=True,
            when=Validator("backup-end.extract.enabled", condition=lambda v: v is True),
            messages={'must_exist_true': 'ERROR: {name} is required when extract is configured'}
        ),
        Validator(
            'backup-end.extract.exclude_storeids',
            default=None,
        ),
    ]
)