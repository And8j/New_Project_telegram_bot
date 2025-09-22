from aiogram import Router

# Import individual routers
from .start import router as start_router
from .help import router as help_router

# Create a main router for the handlers package
router = Router(name=__name__)

# Include all individual routers into the main router
router.include_routers(
    start_router,
    help_router
)

# This line specifies which objects should be exposed when
# someone imports * from this package.
__all__ = ['router']
