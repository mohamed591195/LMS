from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from .fields import OrderField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from comments.models import Comment
from notifications.models import Notify


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug  = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Course(models.Model):
    title         = models.CharField(max_length=200)
    slug          = models.SlugField(max_length=200, unique=True)
    overview      = models.TextField()
    creator       = models.ForeignKey(User, on_delete=models.PROTECT,
                                            related_name='courses_created', 
                                            related_query_name='course_created')
    instructors   = models.ManyToManyField(User, related_name='courses_instructed', 
                                                related_query_name='instruct_in_course', 
                                                blank=True, 
                                                limit_choices_to={'groups__name__in': ['Instructors']}
                                                )
    students      = models.ManyToManyField(User, related_name='courses_enrolled', 
                                                related_query_name='course_enrolled', 
                                                blank=True)
    subject       = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    grade         = models.PositiveIntegerField()
    comments      = GenericRelation(Comment, content_type_field='content_type', object_id_field='object_id', related_query_name='on_course')
    notifications = GenericRelation(Notify, content_type_field='content_type', object_id_field='object_id', related_query_name='on_course')


    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Module(models.Model):
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(max_length=200, unique=True)
    course      = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    description = models.TextField()
    order       = OrderField(for_fields=['course'], blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f'module {self.order +1 } {self.title} for course {self.course}'

class Content(models.Model):
    module       = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, 
                                                  limit_choices_to={'model__in':
                                                                      ('text', 'image', 'file', 'video')})
    object_id    = models.PositiveIntegerField()
    item         = GenericForeignKey('content_type', 'object_id')
    order        = OrderField(blank=True, for_fields=['module'])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_related')
    title   = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def render(self):
        return render_to_string(f'courses/view/{self._meta.model_name}.html', {'item': self})

        
    def __str__(self):
        return self.title

class Text(ItemBase):
    text = models.TextField()

class Image(ItemBase):
    image = models.ImageField()

class Video(ItemBase):
    video_url = models.URLField()

class File(ItemBase):
    ifile = models.FileField(upload_to='files')


# class Grade(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_grads')
#     course  = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students_grads')
#     mark    = models.IntegerField(blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

    

class Assignment(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField()
    ifile       = models.FileField(upload_to='assignment_files/%Y/%m/%d/', blank=True)
    course      = models.ForeignKey(Course, related_name='assignments', related_query_name='assignment', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

