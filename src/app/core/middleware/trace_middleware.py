import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging.logger import trace_id_var, logger

class TraceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate a new unique Trace ID for the incoming request
        trace_id = str(uuid.uuid4())
        
        # Set the trace_id in the context variable
        token = trace_id_var.set(trace_id)
        
        # Record start time
        start_time = time.time()
        
        logger.info(f"Incoming Request: {request.method} {request.url.path}")
        
        try:
            # Process the request
            response = await call_next(request)
            
            # Calculate process time
            process_time = time.time() - start_time
            
            # Add headers to the response
            response.headers["X-Trace-ID"] = trace_id
            response.headers["X-Process-Time"] = f"{process_time:.4f}s"
            
            logger.info(f"Request Completed: {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s")
            return response
            
        except Exception as e:
            # Log unhandled exceptions at the middleware level
            process_time = time.time() - start_time
            logger.error(f"Unhandled Exception on {request.method} {request.url.path} - Time: {process_time:.4f}s - Error: {str(e)}", exc_info=True)
            raise
        finally:
            # Reset the context variable
            trace_id_var.reset(token)
