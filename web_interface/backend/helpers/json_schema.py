from pydantic.json_schema import GenerateJsonSchema


def _get_schema_with_required(json_schema: dict):
    if "$defs" in json_schema:
        for key, _def in json_schema["$defs"].items():
            json_schema['$defs'][key] = _get_schema_with_required(_def)

    if "properties" not in json_schema:
        return json_schema
    else:
        json_schema["required"] = list(json_schema["properties"].keys())
        return json_schema


class JsonSchemaGenerator(GenerateJsonSchema):
    def generate(self, schema, mode='validation'):
        json_schema = super().generate(schema, mode=mode)
        json_schema = _get_schema_with_required(json_schema)

        if "$defs" in json_schema and "CoreSettings" in json_schema["$defs"]:
            json_schema["$defs"]["CoreSettings"]["description"] = "These settings can be changed only in core module."
            for prop_name in json_schema["$defs"]["CoreSettings"]["properties"].keys():
                json_schema["$defs"]["CoreSettings"]["properties"][prop_name]["readOnly"] = True

        return json_schema
