from fastapi.openapi.utils import get_openapi

def custom_openapi(app):
    def custom_schema():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="FastAPI Organized Docs",
            version="1.0.0",
            description="This is a customized OpenAPI schema with well-organized routes.",
            routes=app.routes,
        )
        openapi_schema["info"]["x-logo"] = {
            "url": "https://example.com/logo.png"
        }
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    return custom_schema
