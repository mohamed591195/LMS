from django.test import TestCase
from courses.models import (Course, Subject, Module, Content, Text, File, Image, Video, Assignment)
from django.contrib.auth.models import User


class SubjectModelTest(TestCase):
    def test_saving_and_retrieving_subjects(self):
        sub1 = Subject(title='First Subject', slug='first_subject')
        sub1.save()
        self.assertIsNotNone(sub1)
        saved_sub1 = Subject.objects.first()
        self.assertEqual(sub1, saved_sub1)

        sub2 = Subject(title='Second Subject', slug='second_subject')
        sub2.save()

        saved_subs = Subject.objects.all()
        self.assertEqual(saved_subs.count(), 2)

        self.assertEqual(sub1.title, 'First Subject')
        self.assertEqual(sub2.slug, 'second_subject')

    def test_retriving_subjects_ordered_by_title(self):

        sub2 = Subject(title='B A C', slug='b_a_c')
        sub2.save()

        sub1 = Subject(title='A B C', slug='a_b_c')
        sub1.save()
        
        saved_subs = Subject.objects.all()

        first_sub = saved_subs[0]
        second_sub = saved_subs[1]

        self.assertEqual(first_sub, sub1)
        self.assertEqual(second_sub, sub2)

    def test_auto_save_for_slug(self):

        sub = Subject(title='this is a subject')
        sub.save()
        self.assertEqual(sub.slug, 'this-is-a-subject')

class CourseModelTest(TestCase):

    def setUp(self):
        self.user    = User.objects.create_user(username='instructor', password='testing4321')
        self.subject = Subject.objects.create(title='first subject')

    def test_saving_and_retrieving_courses(self):
        course1 = Course(title='First Course', 
                         slug='first_course', 
                         overview='overview', 
                         creator=self.user,
                         subject=self.subject,
                         grade=50)
        course1.save()
        course1.instructors.add(self.user)
        course1.students.add(self.user) 

        self.assertIsNotNone(course1)
        f_course = Course.objects.first()
        self.assertEqual(f_course, course1)

        course2 = Course(title='Second Course',
                         slug='second_course',
                         overview='overview',
                         creator=self.user,
                         subject=self.subject,
                         grade=200)
        course2.save()
        course2.instructors.add(self.user)
        course2.students.add(self.user)

        courses = Course.objects.all()
        self.assertEqual(courses.count(), 2)

