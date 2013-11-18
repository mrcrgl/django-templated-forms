from django.shortcuts import render
from django.template.loader import render_to_string


class AbstractWidget(object):
    field_instance = None
    arguments = None
    context = None

    def __init__(self, field, arguments=None, context=None):
        self.field_instance = field
        self.arguments = arguments or {}
        self.context = context or None

    def render(self):
        self.arguments['field'] = self.field_instance
        return render_to_string(self.template_name, self.arguments, self.context)
        #return render(self.template_name, self.arguments)


class BooleanField(AbstractWidget):
    template_name = 'templated_forms/widget/boolean_field.html'


class CharField(AbstractWidget):
    template_name = 'templated_forms/widget/char_field.html'


class CheckboxField(AbstractWidget):
    template_name = 'templated_forms/widget/checkbox_field.html'


class DatepickerField(AbstractWidget):
    template_name = 'templated_forms/widget/datepicker_field.html'


class ModelChoiceField(AbstractWidget):
    template_name = 'templated_forms/widget/model_choice_field.html'


class TypedChoiceField(AbstractWidget):
    template_name = 'templated_forms/widget/typed_choice_field.html'


class WidgetFactory(object):

    field_instance = None

    MAPPING = {
        'CheckboxSelectMultiple': (
            CharField,
            {},
        ),
        'ModelChoiceField': (
            ModelChoiceField,
            {},
        ),
        'TypedChoiceField': (
            TypedChoiceField,
            {},
        ),
        'CharField': (
            CharField,
            {'data_type': 'string'},
        ),
        'IntegerField': (
            CharField,
            {'data_type': 'integer'},
        ),
        'FloatField': (
            CharField,
            {'data_type': 'float'},
        ),
        'BooleanField': (
            BooleanField,
            {},
        ),
        'DateTimeField': (
            DatepickerField,
            {'mode': 'datetime'},
        ),
        'DateField': (
            DatepickerField,
            {'mode': 'date'},
        )
    }

    def __init__(self, field_instance):
        self.field_instance = field_instance

    def unbound(self):
        if self.field_instance.__class__.__name__ == "BoundField":
            return self.field_instance.field
        return self.field_instance

    def get_widget_class(self):
        return self.unbound().__class__.__name__

    def get_widget(self):
        class_name = self.get_widget_class()

        try:
            Widget, arguments = WidgetFactory.MAPPING[class_name]
        except KeyError:
            raise NotImplementedError("Widget of type %s is not implemented." % class_name)

        widget = Widget(self.field_instance, arguments)

        return widget