from types import NoneType
from typing import Any
from dotenv import load_dotenv
import os

class LoadDotEnv:

    def __call__(self, *args: Any, **kwds: Any) -> dict:
        load_dotenv(dotenv_path = os.path.abspath(os.getcwd()) + "/.env", override = False)
        return self.__load_vars()

    def __check_vars(self, vars: list) -> bool | NoneType:
        env_items = []

        for name, _ in os.environ.items():
            env_items.append(name)

        for name in vars:

            if "PWMAN_" + name not in env_items:
                return False

    # You can add more variable here, if needed
    def __load_vars(self) -> dict:
        var_list = ["USERNAME", "PASSWORD", "HOST", "PORT", "DATABASE"] # Add vars here
        items = {}

        if self.__check_vars(var_list) != False:
            for x in var_list:
                items[x] = os.getenv("PWMAN_" + x)

            return items
        else:
            raise KeyError("Invalid dotenv! Check that you have all the required configuration values.")
        
