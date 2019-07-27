from django.template import Library
register = Library()


@register.filter
def is_voted(user, comment):
    try:
        return user in comment.votes.all()
    except:
        return None