from os.path import dirname, basename, isfile, join
import glob
import importlib
from config.database import Base  # Do not remove this even if it seems un used
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) is True and not f.endswith('__init__.py')]

for model in __all__:
    importlib.import_module(name = 'database.models.' + model)