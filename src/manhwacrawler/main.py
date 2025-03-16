import logging
import contextlib

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

@contextlib.asynccontextmanager
async def lifespan(app):
    # Startup 
    
    yield
    # Shutdown

async def homepage(request):
    return JSONResponse({'hello': 'world'})


async def detect_bounding_boxes(request):
    logging.debug(request)
    return JSONResponse({"data": "response"})

async def healthcheck(request):
    return JSONResponse({"msg", "ok"})

app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/health', healthcheck),
    Route('/bbox', detect_bounding_boxes)
], lifespan=lifespan)

