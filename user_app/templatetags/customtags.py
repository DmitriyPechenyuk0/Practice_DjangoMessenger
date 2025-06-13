from django import template

register = template.Library()

@register.inclusion_tag(filename= 'user_app/templatetags/custom_form.html', takes_context= True)
def render_custom_form(context):
    return {
        'form': context.get('form'),
        'form_name': context.get('form_name')
    }