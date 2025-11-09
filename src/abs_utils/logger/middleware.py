"""
FastAPI middleware for request logging with context injection
"""

import time
import uuid
from collections.abc import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from abs_utils.logger.core import clear_log_context, get_logger, set_log_context

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for automatic request/response logging

    Automatically adds request_id to log context and logs request details.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and add logging context"""
        # Generate request ID
        request_id = str(uuid.uuid4())

        # Set log context
        set_log_context(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        # Log request start
        start_time = time.time()
        logger.info(
            "Request started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else None,
            },
        )

        try:
            # Process request
            response = await call_next(request)

            # Calculate duration
            duration = time.time() - start_time

            # Log request completion
            logger.info(
                "Request completed",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "duration_seconds": round(duration, 3),
                },
            )

            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as exc:
            # Calculate duration
            duration = time.time() - start_time

            # Log error
            logger.error(
                "Request failed",
                extra={
                    "request_id": request_id,
                    "error": str(exc),
                    "error_type": type(exc).__name__,
                    "duration_seconds": round(duration, 3),
                },
                exc_info=True,
            )
            raise

        finally:
            # Clear log context
            clear_log_context()
