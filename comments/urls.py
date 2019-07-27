from django.urls import path
from comments.views import CreateCommmentView, VoteCommentView

app_name = 'comments'

urlpatterns = [
    path('<slug:course_slug>/', CreateCommmentView.as_view(), name='create_comment_view'),
    path('<slug:course_slug>/<by_voted>/', CreateCommmentView.as_view(), name='create_comment_view_voted'),
        path('<slug:course_slug>/<by_latest>/latest', CreateCommmentView.as_view(), name='create_comment_view_latest'),
    path('vote', VoteCommentView , name='vote_comment_view'),
]