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
            title=self.config['title'] or "ReDoc",
            version=self.config['version'] or "1.0.0",
            openapi_version=self.config['openapi_version'] or "3.0.2",
            info=self.config['info'] or "ReDoc",
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
            print(spec_file)
            return render_template("redoc/index.html", spec_file=spec_file, use_cdn=True)
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
            schema = model.model_json_schema()

            # $defs içindeki referansları değiştir
            if "$defs" in schema:
                defs = schema.pop("$defs")
                for key, value in defs.items():
                    self.spec.components.schema(key, component=value)

                # Tüm referansları düzelt
                def replace_refs(obj):
                    if isinstance(obj, dict):
                        for k, v in obj.items():
                            if isinstance(v, str) and v.startswith("#/$defs/"):
                                obj[k] = v.replace(
                                    "#/$defs/", "#/components/schemas/")
                            else:
                                replace_refs(v)
                    elif isinstance(obj, list):
                        for item in obj:
                            replace_refs(item)

                replace_refs(schema)
            self._add_nested_schemas(schema)
            self.spec.components.schema(model.__name__, component=schema)

    def _add_nested_schemas(self, schema):
        """
        İç içe şemaların components/schemas bölümüne eklenmesini sağlar.
        """
        if 'properties' in schema:
            for field_name, field in schema['properties'].items():
                if '$ref' in field:
                    ref = field['$ref']
                    ref_model_name = ref.split('/')[-1]
                    if ref_model_name not in self.spec.components.schemas:
                        nested_schema = self.spec.components.schemas.get(
                            ref_model_name)
                        if nested_schema:
                            self.spec.components.schema(
                                ref_model_name, component=nested_schema)
                elif 'properties' in field:
                    self._add_nested_schemas(field)
