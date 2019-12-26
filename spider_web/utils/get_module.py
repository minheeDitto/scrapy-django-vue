import importlib
import inspect
import zipfile

def get_modules(module_name):
    module = importlib.import_module(module_name)
    return module

def get_spider_name(module_name):
    module = get_modules(module_name)
    spider_class = inspect.getmembers(module, inspect.isclass)
    real_cls = [cls for cls in spider_class if module_name.rsplit(".",1)[1].title() in cls[0]][0][1]
    return real_cls


