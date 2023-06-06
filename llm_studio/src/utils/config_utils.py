import importlib
from types import ModuleType
from typing import Any


def rreload(module):
    """Recursively reload modules.

    Args:
        module: module to reload
    """

    for attribute_name in dir(module):
        if "Config" in attribute_name:
            attribute1 = getattr(module, attribute_name)
            for attribute_name in dir(attribute1):
                attribute2 = getattr(attribute1, attribute_name)
                if type(attribute2) is ModuleType:
                    importlib.reload(attribute2)


def _load_cls(module_path: str, cls_name: str) -> Any:
    """Loads the python class.

    Args:
        module_path: path to the module
        cls_name: name of the class

    Returns:
        Loaded python class
    """

    module_path_fixed = module_path
    module_path_fixed = module_path_fixed.removesuffix(".py")
    module_path_fixed = module_path_fixed.replace("/", ".")

    module = importlib.import_module(module_path_fixed)
    module = importlib.reload(module)
    rreload(module)
    module = importlib.reload(module)

    assert hasattr(
        module, cls_name
    ), f"{module_path} file should contain {cls_name} class"

    return getattr(module, cls_name)


def load_config(config_path: str, config_name: str = "Config"):
    """Loads the config class.

    Args:
        config_path: path to the config file
        config_name: name of the config class

    Returns:
        Loaded config class
    """

    return _load_cls(config_path, config_name)()
