from django.template import Library
from courses.utils import belong_to_group
from notifications.models import Notify
from itertools import chain
from django.db.models import Q

register = Library()

@register.filter
def count_notifs(user):
    non_admin_verbs = ['Updated the course', 'Deleted the course']
    list_ = None    
    if belong_to_group(user, 'Admins'):
        list_ = list(chain(Notify.objects.filter(on_course__creator=user).\
        exclude(Q(verb__in=non_admin_verbs)), 
        Notify.objects.filter(verb='Created Course'))) 
                

    elif belong_to_group(user, 'Instructors'):
        list_ = list(chain(Notify.objects.filter(on_course__instructors=user),
        Notify.objects.filter(on_comment__on_course__instructors=user)))

    elif user.is_authenticated :
        list_ = list(chain(Notify.objects.filter(on_course__students=user), 
        Notify.objects.filter(on_comment__user=user)))
   
    i = 0
    for n in list_ :
        if user not in n.read_by.all():
            i += 1
    return i 