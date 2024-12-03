from flask import jsonify, render_template
from apispec_webframeworks.flask import FlaskPlugin
from .pydantic_ext import PydanticPlugin
from apispec import APISpec

class Redoc:
    DEFAULT_CONFIG = {
        'title': 'ReDoc',
        'version': '1.0.0',
        'openapi_version': '3.0.2',
        'info': {'title': 'ReDoc', 'version': '1.0.0'},
        'plugins': [FlaskPlugin(), PydanticPlugin()]
    }

    def __init__(self, app=None, spec_file=None, config=None):
        self.app = app
        self.spec_file = spec_file
        self.config = config or self.DEFAULT_CONFIG.copy()
        self.spec = APISpec(
            title=self.config['title'],
            version=self.config['version'],
            openapi_version=self.config['openapi_version'],
            info=self.config['info'],
            plugins=self.config['plugins']
        )

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.config.update(self.app.config.get('REDOC', {}))

        @app.route('/docs/json', methods=['GET'])
        def get_openapi_spec():
            return self.get_spec()


        @app.route("/docs", methods=["GET"])
        def get_redoc():
            spec_file = self.spec.to_dict()
            return render_template("redoc.html", spec_file=spec_file, use_cdn=True)

        self.app.before_request(self.docstrings_to_openapi)

    def docstrings_to_openapi(self):
        for view_name, view_func in self.app.view_functions.items():
            if view_func.__doc__ is not None:
                self.spec.path(view=view_func)

        self.spec_file = self.spec.to_dict()

    def get_spec(self):
        return jsonify(self.spec_file)
    

    def add_schema(self, model):
        self.spec.components.schema(
            model.__name__, component=model.model_json_schema(), )
