import uvicorn

from settings import app_settings
from src.api.app import create_app
from src.utils.logging.config import get_logging_config

app = create_app(settings=app_settings)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=app_settings.PORT,
        log_config=get_logging_config(is_debug=app_settings.IS_DEBUG),
    )
