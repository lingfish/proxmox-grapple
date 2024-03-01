import os
import sys

import pytest

# from tests.dynaconf_config import settings
# from dynaconf import settings
from proxmox_grapple.config import settings



# @pytest.fixture(scope='session', autouse=True)
# def set_test_settings():
#     # current_directory = os.path.dirname(os.path.realpath(__file__))
#     # settings.configure(FORCE_ENV_FOR_DYNACONF='testing', ROOT_PATH_FOR_DYNACONF=current_directory,
#     #                    VALIDATE_ON_UPDATE_FOR_DYNACONF=True
#     #                    )
#     # settings.load_file(path=['proxmox_grapple_tests.yml'], silent=True, validate=True)
#     # import dynaconf
#     # print(dynaconf.inspect_settings(settings, print_report=True, dumper="yaml"))
#     # settings.validators.validate()
#     assert settings.current_env == "testing"