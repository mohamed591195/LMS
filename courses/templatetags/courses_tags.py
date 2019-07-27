from django.template import Library
from courses.utils import belong_to_group
from courses.models import Course


register = Library()

@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except:
        return None

@register.filter
def is_admin(user):
    return belong_to_group(user=user, name='Admins')

@register.filter
def is_instructor(user):
    return belong_to_group(user=user, name='Instructors')


@register.filter
def is_course_instructor(user, course):
    try:
        return user in course.instructors.all()
    except:
        return None

@register.filter
def is_enrolled(user, course):
    try:
        return user in course.students.all()
    except:
        return None