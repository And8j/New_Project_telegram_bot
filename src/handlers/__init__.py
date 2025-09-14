from .start import register_start_handler
from .help import register_help_handler

def register_all_handlers(dp):
    register_start_handler(dp)
    register_help_handler(dp)
