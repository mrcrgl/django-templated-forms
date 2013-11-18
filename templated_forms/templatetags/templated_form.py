from django import template
register = template.Library()

from templated_forms.factory import FormFactory
from templated_forms.nodes import FormFactoryTemplateNode
from pprint import pprint

@register.tag
def parse_form(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, form = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

    return FormFactoryTemplateNode(form)