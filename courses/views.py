from django.shortcuts import render, get_object_or_404, redirect
from courses.models import Course, Module, Content, Subject, Assignment
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count
from .forms import ModuleInlineFormset, AssignmentInlineFormset
from django.http import HttpResponse, HttpResponseRedirect
from .utils import belong_to_group
from django.apps import apps
from django.forms import modelform_factory
from django.contrib.auth.models import User
from notifications.models import Notify
from django.core import serializers
 


class ManageCourseListView(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    template_name = 'courses/manage/course/list.html'
    model = Course
    context_object_name = 'courses'
    permission_required = 'courses.view_course'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(Q(creator=self.request.user) | Q(instructors=self.request.user))

   
class CreateCourseView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'courses/manage/course/form.html'
    model = Course
    fields = ['subject', 'title', 'overview', 'grade', 'instructors', 'students']
    success_url = reverse_lazy('manage_course_list_view')
    permission_required = 'courses.add_course'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        obj = form.save()
        Notify.objects.create(user=self.request.user, verb='Created Course', target=obj)
        return super().form_valid(form)

class UpdateCourseView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'courses/manage/course/form.html'
    model = Course
    fields = ['subject', 'title', 'overview', 'grade', 'instructors', 'students']
    success_url = reverse_lazy('manage_course_list_view')
    permission_required = 'courses.change_course'

    def form_valid(self, form):
        object_ = self.get_object()
        self.object = form.save()

        if str(form) != str(self.get_form_class()(instance=object_, data=None)):
            #will go for its students and instructors
            Notify.objects.create(user=self.request.user, verb='Updated the course', 
                                        target=self.object)
        return HttpResponseRedirect(self.get_success_url())


        
    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)

    

    
class DeleteCourseView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list_view')
    permission_required = 'courses.delete_course'
    model = Course

    def delete(self, request, *args, **kwargs):
  
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        #will go for its instructors and students
        Notify.objects.create(user=self.request.user, verb='Deleted the course', target=self.object)
        return HttpResponseRedirect(success_url)

    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)

class CourseModuleCreateUpdateView(LoginRequiredMixin, PermissionRequiredMixin, TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None
    formset = None
    permission_required = 'courses.add_module'

    def get_formset(self, data=None):
        return ModuleInlineFormset(instance=self.course, data=data)

    def dispatch(self, request, course_id, *args, **kwargs):
        course = get_object_or_404(Course, id=course_id)
        if request.user in course.instructors.all():
            self.course = course
        return super().dispatch(request, course_id, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.course:
            return self.render_to_response({'formset': self.get_formset(), 'course': self.course})
        return HttpResponse('you are allowed as instructor to edit courses you enrolled in only')

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()

            if str(formset) != str(self.get_formset()):   
                #will go for its students, instructors and admin
                Notify.objects.create(user=self.request.user, 
                                        verb='who is the course instructor updated or created modules for his course',  
                                        target=self.course)
            return redirect('manage_course_list_view')
        return self.render_to_response({'formset': formset, 'course': self.course})

class ContentUpdateCreateView(LoginRequiredMixin, PermissionRequiredMixin, TemplateResponseMixin, View):
    template_name = 'courses/manage/content/form.html'
    module = None
    model = None
    form = None
    item_obj = None
    permission_required = 'courses.change_content'
    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None

    def get_form(self, model):
        return modelform_factory(model, exclude=['creator', 'created', 'updated', 'mohamed'])

    def dispatch(self, request, module_id, model_name, item_obj_id=None):
        self.module = get_object_or_404(Module, id=module_id)
        
        if request.user not in self.module.course.instructors.all():
            self.template_name='courses/manage/not_allowed.html'
        self.model = self.get_model(model_name)
        self.form = self.get_form(self.model)
        if item_obj_id:
            self.item_obj = get_object_or_404(self.model, id=item_obj_id)
        return super().dispatch(request, module_id, model_name, item_obj_id)

    def get(self, request, module_id, model_name, item_obj_id):
        form = self.form(instance=self.item_obj)
        module = self.module
        return self.render_to_response({'form': form, 'module': module, 'object': self.item_obj})

    def post(self, request, module_id, model_name, item_obj_id):
        form = self.form(data=request.POST,instance=self.item_obj, files=request.FILES)
        if form.is_valid():
            item_obj = form.save(commit=False)
            item_obj.creator = request.user
            item_obj.save()
            if str(form) != str(self.form(data=None, instance=self.item_obj, files=None)): 
                # will go to its students, instructors and admin  
                Notify.objects.create(user=self.request.user,
                         verb=f'who is instructor updated contents of module {self.module} of his course',
                          target=self.module.course)
            if not item_obj_id:
                #new item so there should be new content
                Content.objects.create(module=self.module, item=item_obj)
            return redirect('course_module_contents_view', self.module.slug)
        return self.render_to_response({'form': form, 'module': self.module})


class CourseModuleContentListView(LoginRequiredMixin, PermissionRequiredMixin, TemplateResponseMixin, View):
    template_name='courses/manage/content/list.html'
    permission_required = 'courses.view_content'

    def get(self,request, module_slug):
        module = get_object_or_404(Module, slug=module_slug)
        return self.render_to_response({'module': module})

class CourseAssignmentCreateUpdateView(LoginRequiredMixin, PermissionRequiredMixin, TemplateResponseMixin,View):
    template_name = 'courses/manage/assignment/create.html'
    permission_required = 'courses.add_assignment'
    course = None

    def get_formset(self, data=None, files=None):
        return AssignmentInlineFormset(instance=self.course, data=data, files=files)

    
    def dispatch(self, request, course_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        if request.user in course.instructors.all():    
            self.course = get_object_or_404(Course, slug=course_slug)            
        return super().dispatch(request, course_slug, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if self.course:
            formset = self.get_formset()
            return self.render_to_response({'formset': formset, 'course': self.course})
        return HttpResponse('you are allowed as instructor to edit courses you enrolled in only')
   
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST, files=request.FILES)
        if formset.is_valid():
            formset.save()
            
            if str(formset) != str(self.get_formset()):
                # will go to its students, instructors and admin
                Notify.objects.create(user=self.request.user,
                                      verb=' who is instructor updated assignemts of his course', 
                                      target=self.course)
        formset = self.get_formset()
        return self.render_to_response({'formset': formset, 'course': self.course}) 




class CourseListView(TemplateResponseMixin, View):
    template_name = 'courses/view/list_courses.html'
    
    def get(self, request, subject_slug=None):
        subject = None
        subjects = Subject.objects.annotate(total_courses=Count('courses'))
        courses = Course.objects.annotate(total_modules=Count('modules'))

        if subject_slug:
            subject = get_object_or_404(Subject, slug=subject_slug)
            courses = courses.filter(subject=subject)
        return self.render_to_response({'courses': courses, 'subject': subject, 'subjects': subjects})

class CourseDetailView(DetailView):
    template_name = 'courses/view/course_detail.html'
    model = Course
    context_object_name = 'course'




