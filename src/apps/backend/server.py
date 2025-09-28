import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask.typing import ResponseReturnValue
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

# Blueprints
from bin.blueprints import api_blueprint, react_blueprint, img_assets_blueprint

# Modules
from modules.account.rest_api.account_rest_api_server import AccountRestApiServer
from modules.application.application_service import ApplicationService
from modules.application.errors import AppError, WorkerClientConnectionError
from modules.application.workers.health_check_worker import HealthCheckWorker
from modules.authentication.rest_api.authentication_rest_api_server import AuthenticationRestApiServer
from modules.config.config_service import ConfigService
from modules.logger.logger_manager import LoggerManager
from modules.task.rest_api.task_rest_api_server import TaskRestApiServer
from modules.comment.rest_api.comment_rest_api_server import CommentRestApiServer
from scripts.bootstrap_app import BootstrapApp
from modules.logger.logger import Logger

load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Mount logger
LoggerManager.mount_logger()

# Run bootstrap tasks
BootstrapApp().run()

# Connect to Temporal Server (optional)

try:
    ApplicationService.connect_temporal_server()

    # Start the health check worker
    ApplicationService.schedule_worker_as_cron(
        cls=HealthCheckWorker, cron_schedule="*/10 * * * *"
    )

except WorkerClientConnectionError as e:
    Logger.critical(message=e.message)



# Apply ProxyFix if behind proxy
if ConfigService.has_value("is_server_running_behind_proxy") and ConfigService[bool].get_value(
    "is_server_running_behind_proxy"
):
    app.wsgi_app = ProxyFix(app.wsgi_app)  # type: ignore

# Register API blueprints
api_blueprint.register_blueprint(AuthenticationRestApiServer.create())
api_blueprint.register_blueprint(AccountRestApiServer.create())
api_blueprint.register_blueprint(TaskRestApiServer.create())
api_blueprint.register_blueprint(CommentRestApiServer.create())

app.register_blueprint(api_blueprint)

# Register React frontend blueprints
app.register_blueprint(react_blueprint)
app.register_blueprint(img_assets_blueprint)


# Global error handler
@app.errorhandler(AppError)
def handle_app_error(exc: AppError) -> ResponseReturnValue:
    return jsonify({"message": exc.message, "code": exc.code}), exc.http_code or 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
