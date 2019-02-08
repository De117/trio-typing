# Adapts mypy.test.data pytest plugin for use outside the mypy tree

import os
import sys
import types

data_prefix = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "trio_typing/_tests/test-data"
)


class ConfigModule(types.ModuleType):
    def __init__(self) -> None:
        self.test_data_prefix = data_prefix
        self.PREFIX = os.path.dirname(os.path.realpath(__file__))
        self.test_temp_dir = "tmp"


sys.modules["mypy.test.config"] = ConfigModule()

from mypy.test.data import *
