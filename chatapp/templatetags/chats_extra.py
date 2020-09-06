from django import template

register = template.Library()


@register.simple_tag()
def other_member(user_chat, user):
    if user_chat.member_one == user:
        return user_chat.member_two.username
    else:
        return user_chat.member_one.username
