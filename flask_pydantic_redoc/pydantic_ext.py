from pydantic import BaseModel
from apispec import BasePlugin


class PydanticPlugin(BasePlugin):
    def __init__(self):
        self.processed_models = {}

    def schema_helper(self, name, definition, **kwargs):
        if isinstance(definition, type) and issubclass(definition, BaseModel):
            return self._process_model(definition)

        return definition

    def _process_model(self, model):
        if model.__name__ in self.processed_models:
            return self.processed_models[model.__name__]

        schema = {
            'type': 'object',
            'properties': {},
            'title': model.__name__
        }

        for field_name, field in model.model_fields.items():
            schema['properties'][field_name] = self._process_field(field)

        self.processed_models[model.__name__] = schema
        return schema

    def _process_field(self, field):
        field_info = {}

        origin_type = field.annotation

        if hasattr(origin_type, '__origin__'):
            if origin_type.__origin__ is list:
                field_info['type'] = 'array'
                field_info['items'] = self._process_type(
                    origin_type.__args__[0])
            elif origin_type.__origin__ is dict:
                field_info['type'] = 'object'
                field_info['additionalProperties'] = self._process_type(
                    origin_type.__args__[1])
        else:
            field_info.update(self._process_type(origin_type))

        if field.description:
            field_info['description'] = field.description

        return field_info

    def _process_type(self, type_hint):
        if isinstance(type_hint, type) and issubclass(type_hint, BaseModel):
            return {
                'type': 'object',
                '$ref': f'#/components/schemas/{type_hint.__name__}'
            }

        type_map = {
            str: {'type': 'string'},
            int: {'type': 'integer'},
            float: {'type': 'number'},
            bool: {'type': 'boolean'},
            list: {'type': 'array'},
            dict: {'type': 'object'}
        }

        return type_map.get(type_hint, {'type': 'string'})