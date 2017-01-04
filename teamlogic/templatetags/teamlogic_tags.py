from django import template


register = template.Library()

@register.inclusion_tag('tools/pager.html', takes_context=True)
def pager(context):
    show_pager = (context['is_paginated'] and
                  context['paginator'].num_pages > 1)

    if not show_pager:
        return locals()

    page = context['page_obj']
    current_page = page.number
    previous_page = page.number - 1
    following_page = page.number + 1

    previoues_pages = []
    following_pages = []

    for i in range(1, 4):
        if current_page - i > 1:
            previoues_pages.append(current_page - i)
        elif current_page - i == 1:
            previoues_pages.append(current_page - i)
            break
        else:
            break
    previoues_pages.reverse()

    for i in range(1, 4):
        if current_page + 1 < context['paginator'].num_pages:
            following_pages.append(current_page + i)
        elif current_page + 1 == context['paginator'].num_pages:
            following_pages.append(current_page + i)
            break
        else:
            break

    return locals()
