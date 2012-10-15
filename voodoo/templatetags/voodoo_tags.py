from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.core.urlresolvers import reverse, NoReverseMatch
from django import template

register = template.Library()

site = admin.site

def get_app_list(request):
    """
    Return install app
    """
    app_dict = {}
    user = request.user
    for model, model_admin in site._registry.items():
        app_label = model._meta.app_label
        has_module_perms = user.has_module_perms(app_label)

        if has_module_perms:
            perms = model_admin.get_model_perms(request)
            if True in perms.values():
                info = (app_label, model._meta.module_name)
                model_dict = {
                    'name': capfirst(model._meta.verbose_name_plural),
                    'perms': perms,
                    }
                if perms.get('change', False):
                    try:
                        model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=model.__name__.lower())
                    except NoReverseMatch:
                        pass
                if perms.get('add', False):
                    try:
                        model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=model.__name__.lower())
                    except NoReverseMatch:
                        pass
                if app_label in app_dict:
                    app_dict[app_label]['models'].append(model_dict)
                else:
                    app_dict[app_label] = {
                        'name': app_label.title(),
                        'app_url': reverse('admin:app_list', kwargs={'app_label': app_label}),
                        'has_module_perms': has_module_perms,
                        'models': [model_dict],
                        'app_label': app_label,
                        }

    app_list = app_dict.values()
    app_list.sort(lambda x, y: cmp(x['name'], y['name']))

    try:
        from django.conf import settings as django_settings
        if hasattr(django_settings, 'VOODOO_MENU'):
            ex_app = django_settings.VOODOO_MENU
        else:
            ex_app = {}
    except ImportError, exp:
        ex_app = {}

    return {'adm_app_list': app_list, 'ex_app': ex_app}

@register.inclusion_tag('admin/main_menu.html', takes_context=True)
def main_menu(context):
    request = context['request']
    return get_app_list(request)