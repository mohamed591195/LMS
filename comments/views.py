from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from comments.models import Comment
from .forms import CommentForm
from courses.models import Course
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from common.decorators import is_ajax
from django.http import JsonResponse
from django.db.models import Count
from notifications.models import Notify

class CreateCommmentView(LoginRequiredMixin, FormView):
    form_class = CommentForm
    template_name = 'comments/course_discussion.html'
    course = None
   
    def get(self, request, course_slug, by_voted=None, by_latest=None):
        self.course = get_object_or_404(Course, slug=course_slug)
       
        if by_voted:
            comments = self.course.comments.annotate(total_votes=Count('votes')).order_by('-total_votes')
        elif by_latest:
            comments = self.course.comments.all().order_by('-created_at')
        else:
            comments = self.course.comments.all()
        self.extra_context = {'course': self.course, 'comments': comments}
        return super().get(request, course_slug)

    def post(self, request, course_slug ):
        form = self.get_form()
        if form.is_valid():
            comment = request.POST['comment']
            if comment != None and comment != '':
                if 'course_id' in request.POST:
                    course = get_object_or_404(Course, id=request.POST.get('course_id'))
                    cc = Comment.objects.create(user=request.user, target=course, comment=comment)
                    Notify.objects.create(user=request.user, verb='commented on the course', target=course)
                elif 'comment_id' in request.POST:
                    comment_obj = get_object_or_404(Comment, id=request.POST.get('comment_id'))
                    Comment.objects.create(user=request.user, target=comment_obj, comment=comment)
                    Notify.objects.create(user=request.user, verb='replied on your comment', target=comment_obj)
        return redirect('comments:create_comment_view', course_slug)
        

@login_required
@require_POST
@is_ajax
def VoteCommentView(request):
    
    comment_id = request.POST.get('comment_id')
    comment =  get_object_or_404(Comment, id=comment_id)
    user = request.user
    if user in comment.votes.all():
        comment.votes.remove(user)
        action = 'vote up'
    else:
        comment.votes.add(user)
        action = 'remove vote'
        Notify.objects.create(user=request.user, verb='voted up your comment', target=comment)
    votes = comment.votes.all().count()
    return JsonResponse({'votes': votes, 'action': action})
