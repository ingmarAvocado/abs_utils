#!/usr/bin/env python3
"""
FastAPI with logging middleware example
"""
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from abs_utils.logger import setup_logging, get_logger, LoggingMiddleware
from abs_utils.exceptions import NotaryException, DocumentNotFoundException


# Setup logging at app startup
setup_logging(level="INFO", log_format="json", service_name="fastapi-example")

# Create FastAPI app
app = FastAPI(title="Example API")

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Get logger
logger = get_logger(__name__)


# Exception handler for NotaryException
@app.exception_handler(NotaryException)
async def handle_notary_exception(request, exc: NotaryException):
    """Convert NotaryException to JSON response"""
    logger.error(f"NotaryException: {exc.message}", extra=exc.to_dict())
    return JSONResponse(
        status_code=400,
        content=exc.to_dict()
    )


@app.get("/")
async def root():
    """Root endpoint"""
    logger.info("Root endpoint called")
    return {"message": "Hello World"}


@app.get("/documents/{doc_id}")
async def get_document(doc_id: int):
    """Get document by ID"""
    logger.info(f"Getting document {doc_id}")

    if doc_id == 0:
        # Raise custom exception
        raise DocumentNotFoundException(doc_id)

    return {"document_id": doc_id, "status": "found"}


@app.post("/process")
async def process_data(data: dict):
    """Process incoming data"""
    logger.info("Processing data", extra={"data_keys": list(data.keys())})

    # Simulate processing
    if "error" in data:
        logger.error("Processing failed", extra={"reason": data["error"]})
        raise HTTPException(status_code=400, detail="Processing failed")

    return {"status": "processed", "data": data}


if __name__ == "__main__":
    import uvicorn

    # Run with: python fastapi_logging.py
    # Then visit: http://localhost:8000/docs
    uvicorn.run(app, host="0.0.0.0", port=8000)