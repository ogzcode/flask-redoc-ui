from flask import jsonify, render_template, Blueprint
from apispec_webframeworks.flask import FlaskPlugin
from .pydantic_ext import PydanticPlugin
from apispec import APISpec


class Redoc:
    DEFAULT_CONFIG = {
        'title': 'ReDoc',
        'version': '1.0.0',
        'openapi_version': '3.0.2',
        'info': {'title': 'ReDoc', 'version': '1.0.0'}
    }

    def __init__(self, app=None, spec_file=None, config=None, schemas=[]):
        self.app = app
        self.spec_file = spec_file
        self.config = config or self.DEFAULT_CONFIG.copy()
        self.schemas = schemas
        self.spec = APISpec(
            title=self.config['title'],
            version=self.config['version'],
            openapi_version=self.config['openapi_version'],
            info=self.config['info'],
            plugins=[FlaskPlugin(), PydanticPlugin()]
        )
        self._is_initialized = False
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.config.update(self.app.config.get('REDOC', {}))

        self.app.before_request(self.docstrings_to_openapi)

        redoc_bp = Blueprint('redoc', __name__, template_folder='templates')

        self.app.before_request(self.docstrings_to_openapi)

        @redoc_bp.route('/docs/json', methods=['GET'])
        def get_openapi_spec():
            return self.get_spec()

        @redoc_bp.route("/docs", methods=["GET"])
        def get_redoc():
            spec_file = self.spec.to_dict()
            return render_template("redoc.html", spec_file=spec_file, use_cdn=True)

        self.app.register_blueprint(redoc_bp)

    def docstrings_to_openapi(self):
        if self._is_initialized:
            return

        for schema in self.schemas:
            self.add_schema(schema)

        for view_name, view_func in self.app.view_functions.items():
            if view_func.__doc__ is not None:
                self.spec.path(view=view_func)

        self.spec_file = self.spec.to_dict()
        self._is_initialized = True

    def get_spec(self):
        return jsonify(self.spec_file)

    def add_schema(self, model):
        if model.__name__ not in self.spec.components.schemas:
            self.spec.components.schema(
                model.__name__, component=model.model_json_schema(), )
