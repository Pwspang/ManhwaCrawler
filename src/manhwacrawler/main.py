from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


async def homepage(request):
    return JSONResponse({'hello': 'world'})


async def detect_bounding_boxes(request):
    return JSONResponse({"data: response"})

app = Starlette(debug=True, routes=[
    Route('/', homepage),
])