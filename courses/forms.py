from django.forms import inlineformset_factory
from courses.models import Module, Course, Assignment

ModuleInlineFormset = inlineformset_factory(Course, Module, extra=2, 
                                            fields=['title', 'description'], can_delete=True)

AssignmentInlineFormset = inlineformset_factory(Course, Assignment, extra=2, 
                                                fields=['title', 'description', 'ifile'], can_delete=True)