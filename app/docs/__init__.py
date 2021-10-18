from flask_swagger_ui import get_swaggerui_blueprint


swagger_ui = get_swaggerui_blueprint(
            '/docs',
            '/static/swagger.json',
            config={
                "app_name": "videoApi"
            }
)
