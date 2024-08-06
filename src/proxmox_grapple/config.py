from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    settings_files=['proxmox_grapple.yml', '/etc/proxmox_grapple.yml'],
    environments=True,
    env='production',
    apply_default_on_none=True,
    core_loaders=['YAML'],
    validators=[
        Validator('job-init', 'job-start', 'job-end', 'job-abort', 'backup-start', 'backup-end', 'backup-abort',
                  'log-end', 'pre-stop', 'pre-restart', 'post-restart',
                  is_type_of=dict),

        Validator('job-init.mode', 'job-init.run',
                  must_exist=True,
                  when=Validator('job-init', must_exist=True)
                  ),
        Validator('job-start.mode', 'job-start.run',
                  must_exist=True,
                  when=Validator('job-start', must_exist=True)
                  ),
        Validator('job-end.mode', 'job-end.run',
                  must_exist=True,
                  when=Validator('job-end', must_exist=True)
                  ),
        Validator('job-abort.mode', 'job-abort.run',
                  must_exist=True,
                  when=Validator('job-abort', must_exist=True)
                  ),
        Validator('backup-start.mode', 'backup-start.run',
                  must_exist=True,
                  when=Validator('backup-start', must_exist=True)
                  ),
        Validator('backup-end.mode', 'backup-end.run',
                  must_exist=True,
                  when=Validator('backup-end', must_exist=True)
                  ),
        Validator('backup-abort.mode', 'backup-abort.run',
                  must_exist=True,
                  when=Validator('backup-abort', must_exist=True)
                  ),
        Validator('log-end.mode', 'log-end.run',
                  must_exist=True,
                  when=Validator('log-end', must_exist=True)
                  ),
        Validator('pre-stop.mode', 'pre-stop.run',
                  must_exist=True,
                  when=Validator('pre-stop', must_exist=True)
                  ),
        Validator('pre-restart.mode', 'pre-restart.run',
                  must_exist=True,
                  when=Validator('pre-restart', must_exist=True)
                  ),
        Validator('post-restart.mode', 'post-restart.run',
                  must_exist=True,
                  when=Validator('post-restart', must_exist=True)
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