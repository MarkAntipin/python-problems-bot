import uvicorn

from settings import AppSettings
from src.api.app import create_app
from src.utils.logger import setup_logger

app_settings = AppSettings()
app = create_app(settings=app_settings)

if __name__ == "__main__":
    setup_logger()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=app_settings.PORT,
    )
