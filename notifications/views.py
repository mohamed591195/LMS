from django.shortcuts import render, get_object_or_404
from .models import Notify
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.models import User
from courses.utils import belong_to_group
from courses.models import Course, Module
from django.db.models import Q
from itertools import chain



class ListNotifications(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'notifications/list.html'
    non_admin_verbs = ['Updated the course', 'Deleted the course']


    def get(self, request, *args, **kwargs):
        notifications = None

        if belong_to_group(self.request.user, 'Admins'):
            notifications = list(chain(Notify.objects.filter(on_course__creator=self.request.user).\
            exclude(Q(verb__in=self.non_admin_verbs)), 
            Notify.objects.filter(verb='Created Course'))) 
            

        elif belong_to_group(self.request.user, 'Instructors'):
            notifications = list(chain(Notify.objects.filter(on_course__instructors=self.request.user),
            Notify.objects.filter(on_comment__on_course__instructors=self.request.user)))
        
        elif self.request.user.is_authenticated :
            notifications = list(chain(Notify.objects.filter(on_course__students=self.request.user), 
            Notify.objects.filter(on_comment__user=self.request.user)))
        

        for n in notifications:
            if self.request.user not in n.read_by.all():
                n.read_by.add(self.request.user)
       
        return self.render_to_response({'notifications': notifications})

    


