from django.contrib.admin.templatetags.admin_list import (
    ResultList, items_for_result,
    result_headers, result_hidden_fields
)

from django.template import Library
register = Library()


def results(cl):
    if cl.formset:
        for res, form in zip(cl.result_list, cl.formset.forms):
            yield ResultList(form, items_for_result(cl, res, form))
    else:
        for res in cl.result_list:
            yield ResultList(None, items_for_result(cl, res, None))


@register.inclusion_tag("admin/change_list_cards.html")
def card_list(cl,cards):
    return {'cards': cards}


@register.simple_tag
def get_icon(name):
    icons = {
        'Jobs': 'briefcase',
        'Reports': 'briefcase',
        'Programs': 'box',
        'Users': 'users',
        'Fund Accounts': 'archive',
        'Bounties': 'dollar-sign',
        'Notifications': 'bell'
    }
    return icons[name] if name in icons else 'box'

@register.filter
def lookup(d, key):
    # try:
    #    print(d[key])
    # except Exception as e:
    #    print(e)
    # print(d[key] if d[key] else 'p')
    if key not in d:
        return None
    return d[key]


@register.filter()
def check_permission(user, permission):
    if user.user_permissions.filter(codename = permission).exists():
        return True
    return False