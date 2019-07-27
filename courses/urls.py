from django.urls import path, include
from courses import views

urlpatterns = [
   path('manage/', include([
        path('', views.ManageCourseListView.as_view(), name='manage_course_list_view'),
        path('create/', views.CreateCourseView.as_view(), name='course_create_view'),
        path('update/<slug:slug>/', views.UpdateCourseView.as_view(), name='course_update_view'),
        path('delete/<slug:slug>/', views.DeleteCourseView.as_view(), name='course_delete_view'),
        path('edit_course_modules/<course_id>/', views.CourseModuleCreateUpdateView.as_view(), 
                                                                        name='course_modules_create_view'),
        path('module/<int:module_id>/content/<model_name>/create/', views.ContentUpdateCreateView.as_view(),
                                                                        name='content_create_view' ),
        path('module/<int:module_id>/content/<model_name>/update/<int:item_obj_id>/',
                                                                    views.ContentUpdateCreateView.as_view(),
                                                                    name='content_update_view'),
                                                               
         path('module/<slug:module_slug>/contents/', views.CourseModuleContentListView.as_view(), 
                                                               name='course_module_contents_view'),
        
   ])),

   path('', views.CourseListView.as_view(), name='course_list_view'),
   path('<slug:subject_slug>/', views.CourseListView.as_view(), name='subject_courses_list_view'),
   path('detail/<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail_view'),
   path('edit_course_assigments/<course_slug>/', views.CourseAssignmentCreateUpdateView.as_view(),
                                                               name='course_assignments_create_view')
      
    
]