from django.shortcuts import render, get_object_or_404, redirect
from .forms import Register, AccountEditForm, UserEditForm, SearchUsersForm
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.models import Group
from courses.models import Course, Assignment
from courses.utils import belong_to_group
from django.contrib.auth import authenticate, login

class CreateUser(CreateView):
    form_class = Register
    template_name = 'users/register.html'
    success_url = reverse_lazy('course_list_view')

    def form_valid(self, form):
        self.object = form.save()
        cd = form.cleaned_data
        user = authenticate(self.request, username=cd['username'], password=cd['password2'])
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


@login_required
def EditUserInfo(request):
    user = request.user
    if user:
        try:
            if request.method == 'POST':
                a_form = AccountEditForm(data=request.POST, files=request.FILES, instance=user.sys_user)
                u_form = UserEditForm(data=request.POST, instance=user)
                if a_form.is_valid() and u_form.is_valid():
                    a_form.save()
                    u_form.save()
                    messages.success(request, f'your account have updated successfully {user.get_full_name()}')
            else:
                a_form = AccountEditForm(instance=user.sys_user)
                u_form = UserEditForm(instance=user)
            return render(request, 'users/account_settings.html', {'u_form': u_form, 'a_form': a_form})
        except:
            return HttpResponse("<h1>Some thing went wrong, try contacting admins</h1>")
    else:
        return HttpResponse(" it's forbidden, You are not allowed to see this page")


class UsersManageList(LoginRequiredMixin, PermissionRequiredMixin, TemplateResponseMixin, View):
    template_name = 'users/manage/users_list.html'
    permission_required = 'auth.view_user'
    form = SearchUsersForm
    users = User.objects.exclude(groups__name__in=['Admins']).exclude(is_superuser=True)

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'users': self.users, 'form': self.form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            q = form.cleaned_data['user']
            users = self.users.filter(Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q))
            return self.render_to_response({'users': users, 'form': form})
        return self.render_to_response({'users': self.users, 'form': form})


class DeleteUserView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'users/manage/delete_user.html'
    success_url = reverse_lazy('manage_users_list_view')
    permission_required = 'auth.delete_user'
    model = User
    
class PromoteToInstructor(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'auth.delete_user'
    def post(self, request, pk,*args, **kwargs):
        user = get_object_or_404(User, id=pk)
        ins = Group.objects.get(name='Instructors')
        if user.groups.filter(name='Instructors').exists():
            user.groups.remove(ins)
        else:
            user.groups.add(ins)
        return redirect('manage_users_list_view')

class InstructorCoursesList(ListView):
    template_name = 'users/courses/instructor_courses.html'
    context_object_name = 'courses'

    def get_queryset(self):
        instructor = User.objects.get(id=self.kwargs.get('pk'))
        self.extra_context = {
        'instructor': instructor
        }
        return Course.objects.filter(instructors=instructor)


@login_required
def CourseEnrollView(request, pk):

    course = Course.objects.get(id=pk)
    course.students.add(request.user)
    return redirect('course_detail_view', course.slug)


        

class StudentCourseListView(LoginRequiredMixin, ListView):
    template_name = 'users/courses/course_list.html'
    model = Course
    context_object_name = 'courses'

    def get_queryset(self):
        return super().get_queryset().filter(students=self.request.user)


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    template_name = 'users/courses/course_detail.html'
    model = Course
    context_object_name = 'course'
    
    def get_queryset(self):
        if belong_to_group(self.request.user, 'Admins'):
            return super().get_queryset()
        return super().get_queryset().filter(Q(students=self.request.user) | Q(instructors=self.request.user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id=self.kwargs.get('module_id'))
        else:
            context['module'] = course.modules.first()

        return context

class CourseAssigmentsListView(LoginRequiredMixin, ListView):
    template_name = 'users/courses/assignments_list.html'
    model = Assignment
    context_object_name = 'assignments'


    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return super().get_queryset().filter(Q(course__instructors=self.request.user) | Q(course__students=self.request.user),
                                            course=course,)