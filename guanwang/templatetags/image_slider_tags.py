from django import template

from ..models import SliderImage

register = template.Library()


def get_slider_items(parser,token):
    """Returns the published slider items."""
    try:
        tag_name, item_name = token.split_contents()
    except:
        raise template.TemplateSyntaxError("%r tag requires exactly one argument" % token.contents.split()[0])
    return SliderItemObject(item_name)


class SliderItemObject(template.Node):
    def __init__(self, item_name):
        self.item_name = item_name

    def render(self, context):
        slider_item = SliderImage.objects.all()
        return {'slider_items', slider_item}


register.tag('slider_items', get_slider_items)
