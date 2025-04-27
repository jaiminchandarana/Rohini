import importlib
import sys
def dynamic_import(module_name):
    if module_name not in sys.modules:
        globals()[module_name] = importlib.import_module(module_name)
    return sys.modules[module_name] 