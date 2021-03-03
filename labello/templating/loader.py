from jinja2 import Environment, BaseLoader, TemplateNotFound, meta
from labello.database import Label
from labello.templating import epl


class DatabaseLoader(BaseLoader):
    def __init__(self):
        pass

    def get_source(self, environment, template_id):
        label = Label.select().where(Label.id == template_id).get()
        if label is None:
            raise TemplateNotFound(template_id)

        source = label.raw
        return source, template_id, lambda: True


jinja_env = Environment(
    loader=DatabaseLoader(),
)

jinja_env.globals["epl"] = epl
print(jinja_env.globals)


def get_variables(env, template_id):
    template_source = env.loader.get_source(env, template_id)
    parsed_content = env.parse(template_source)
    return meta.find_undeclared_variables(parsed_content)
