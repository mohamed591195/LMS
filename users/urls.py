from django.urls import path, include
from users import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy



urlpatterns = [
    path('register/', views.CreateUser.as_view(), name='register_view'),
    path('update_info/', views.EditUserInfo, name='update_info_view'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login_view'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout_view'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/pass_change.html',
        success_url=reverse_lazy('pass_change_done_view')), 
        name='pass_change_view'),

    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/pass_change_done.html'),
        name='pass_change_done_view'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/pass_reset.html',
        success_url=reverse_lazy('pass_reset_complete_view'),
        email_template_name='users/pass_reset_email.html'), 
        name='pass_reset_view'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/pass_reset_complete.html'),
        name='pass_reset_complete_view'),

    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/pass_reset_confirm.html',
        success_url='pass_reset_done_view'),
        name='pass_reset_confirm_view'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/pass_reset_done.html'),
        name='pass_reset_done_view'),
        

    path('manage/', include([
        path('', views.UsersManageList.as_view(), name='manage_users_list_view'),
        path('delete/<int:pk>/', views.DeleteUserView.as_view(), name='delete_user_view'),
        path('privilege/<int:pk>/', views.PromoteToInstructor.as_view(), name='instructor_privilege_view'),
        

    ])),

    path('enroll/<int:pk>/', views.CourseEnrollView, name='course_enroll_view'), 
    path('instructor/<int:pk>/', views.InstructorCoursesList.as_view(), name='instructor_courses_list_view'),
    path('courses/', views.StudentCourseListView.as_view(), name='student_course_list_view'),
    path('course/<int:pk>/', views.StudentCourseDetailView.as_view(), name='student_course_detail_view'),
    path('course/<int:pk>/<int:module_id>/',views.StudentCourseDetailView.as_view(), 
                                            name='student_course_module_detail_view'),

    path('course/<int:course_id>/assignments/', views.CourseAssigmentsListView.as_view(), name='course_assignments_list_view')
    

   

    


]