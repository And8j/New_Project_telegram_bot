# src/handlers/__init__.py

from .start import router as start_router
from .help import router as help_router

# list of routers for Dispatcher
routers = [
    start_router,
    help_router,
]
