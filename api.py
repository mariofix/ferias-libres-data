import os

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.flask import FlaskIntegration

from ferias_libres import create_app

load_dotenv()

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN", None),
    integrations=[
        FlaskIntegration(),
    ],
    traces_sample_rate=float(os.environ.get("SENTRY_SAMPLE_RATE", 1.0)),
    release=os.environ.get("SENTRY_RELEASE", None),
    environment=os.environ.get("SENTRY_DSN", None),
    attach_stacktrace=True,
    send_default_pii=True,
)
app_settings_file = os.getenv("FLASK_APP_SETTINGS_FILE")
flask_app = create_app(app_settings_file)

if __name__ == "__main__":
    flask_app.run()
