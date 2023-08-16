class CommonSettings:
    @classmethod
    def get_dict(cls, *exclude_fields):
        props_dict = {}
        exclude_fields = list(exclude_fields)
        exclude_fields.append('get_dict')

        props = [prop for prop in dir(cls) if not prop.startswith('__')]
        for field in exclude_fields:
            if field in props:
                props.remove(field)

        for prop in props:
            if isinstance(getattr(cls, prop), CommonSettings):
                props_dict[prop] = getattr(cls, prop).get_dict()
            else:
                props_dict[prop] = getattr(cls, prop)

        return props_dict
