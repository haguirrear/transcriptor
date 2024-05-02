from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware


class NotFoundRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Check if the response status code is 404
        if response.status_code == 404:
            # Redirect to the /404 page
            return RedirectResponse(url="/404")

        # Return the response if the status code is not 404
        return response
