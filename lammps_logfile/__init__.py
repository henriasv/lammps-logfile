from .File import File
from .utils import running_mean, get_color_value, get_matlab_color
from .cmd_interface import run
try:
    from .reader import read_log
except ImportError:
    pass