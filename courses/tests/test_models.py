from django.test import TestCase
from courses.models import (Course, Subject, Module, Content, Text, File, Image, Video, Assignment)
from django.contrib.auth.models import User
from django.core.files import File
import mock

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

    def test_auto_save_for_subject_slug(self):

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

        s_course = Course.objects.all()[1]

        courses = Course.objects.all()
        self.assertEqual(courses.count(), 2)

        self.assertEqual(f_course.slug, course1.slug)
        self.assertEqual(s_course.title, course2.title)

        
    def test_retriving_courses_ordered_by_title(self):
        course1 = Course(title='B A C',
                         slug='first_course',
                         overview='overview',
                         creator=self.user,
                         subject=self.subject,
                         grade=200)
        course1.save()
        course1.instructors.add(self.user)
        course1.students.add(self.user)

        course2 = Course(title='A B C',
                         slug='second_course',
                         overview='overview',
                         creator=self.user,
                         subject=self.subject,
                         grade=200)
        course2.save()
        course2.instructors.add(self.user)
        course2.students.add(self.user)

        courses = Course.objects.all()
        f_course = courses[0]
        s_course = courses[1]
        self.assertEqual(f_course, course2)
        self.assertEqual(s_course, course1)

    def test_auto_save_for_course_slug(self):
        course = Course(title='B A C',
                         overview='overview',
                         creator=self.user,
                         subject=self.subject,
                         grade=200)
        course.save()
        self.assertEqual(course.slug, 'b-a-c')

class ModuleModelTest(TestCase):
    def setUp(self):
        self.user    = User.objects.create_user(username='instructor', password='testing4321')
        self.subject = Subject.objects.create(title='first subject')
        self.course  = Course(title='B A C',
                         overview='overview',
                         creator=self.user,
                         subject=self.subject,
                         grade=200)
        self.course.save()

    def test_saving_and_retrieving_modules(self):

        module1 = Module(title='First Module', 
                         slug='first_module',
                         course=self.course,
                         description='description',
                         )
        module1.save()
        self.assertIsNotNone(module1)
  
        saved_module1 = Module.objects.first()
        self.assertEqual(saved_module1, module1)

        module2 = Module(title='Second Module', 
                         slug='second_module',
                         course=self.course,
                         description='description',
                         )
        module2.save()
        
        modules = Module.objects.all()
        self.assertEqual(modules.count(), 2)
        saved_module2 = Module.objects.all()[1]

        self.assertEqual(saved_module1.title, module1.title)
        self.assertEqual(saved_module2.slug, module2.slug)

    def test_saving_modules_orderd_to_course_field(self):
     
        course1 = Course(title='First Course', 
                         slug='first_course', 
                         overview='overview', 
                         creator=self.user,
                         subject=self.subject,
                         grade=50)
        course1.save()
        course2 = Course(title='Second Course',
                         slug='second_course',
                         overview='overview',
                         creator=self.user,
                         subject=self.subject,
                         grade=200)
        course2.save()

        module1_course1 = Module(title='First Module',
                         slug='first-module',
                         course=course1,
                         description='description',
                         )

        module1_course1.save()
        module2_course1 = Module(title='Second Module',
                                 slug='second_module',
                                 course=course1,
                                 description='descriptoin')
        module2_course1.save()
        self.assertEqual(module1_course1.order, 0)
        self.assertEqual(module2_course1.order, 1)

        module1_course2 = Module(title='Second Moudle',
                                 slug='second-module',
                                 course=course2,
                                 description='description')
        module1_course2.save()
        self.assertEqual(module1_course2.order, 0)

    def test_auto_save_for_module_slug(self):
        module =  Module(title='First Module', 
                         course=self.course,
                         description='description',
                         )
        module.save()
        self.assertEqual(module.slug, 'first-module')

    def test_retriving_modules_ordered_by_order(self):
        module1 = Module.objects.create(title='First Module', 
                         course=self.course,
                         order= 10,
                         description='description',
                         )
    
        module2 = Module.objects.create(title='Second Module', 
                         course=self.course,
                         order= 8,
                         description='description',
                         )
        modules = Module.objects.all()
        self.assertEqual(module1, modules[1])
        self.assertEqual(module2, modules[0])

class ContentModelTest(TestCase):
    def setUp(self):
        user        = User.objects.create_user(username='instructor', password='testing4321')
        subject     = Subject.objects.create(title='first subject')
        self.course      = Course.objects.create(title='B A C', overview='overview', creator=user, subject=subject, grade=200)
        self.module = Module.objects.create(title='First Module', course=self.course, description='description')
        self.text   = Text.objects.create(title='text-title', creator=user, text='text')
        self.video  = Video.objects.create(title='video', creator=user, video_url='www.example.com')

    def test_saving_and_retrieving_contents(self):
        content1 = Content.objects.create(module=self.module, item=self.text)

        self.assertIsNotNone(content1)
        saved_content1 = Content.objects.first()
        self.assertEqual(content1, saved_content1)
        
        content2 = Content.objects.create(module=self.module, item=self.video)
        
        saved_contents = Content.objects.all()
        self.assertEqual(saved_contents.count(), 2)
        
        saved_content1 = saved_contents[0]
        saved_content2 = saved_contents[1]
        self.assertEqual(saved_content1.item, content1.item)
        self.assertEqual(saved_content2.item, content2.item)

    def test_saving_contents_ordered_to_module_field(self):
        module1 = Module.objects.create(title='FFirst Module', course=self.course, description='description')
        module2 = Module.objects.create(title='Second Module', course=self.course, description='dd')
        
        content1 = Content.objects.create(module=module1, item=self.video)
        content2 = Content.objects.create(module=module2, item=self.video)
        content3 = Content.objects.create(module=module1, item=self.video)
        self.assertEqual(content1.order, 0)
        self.assertEqual(content2.order, 0)
        self.assertEqual(content3.order, 1)

    def test_retriving_contents_ordered_by_order(self):
        content1 = Content.objects.create(module=self.module, order=200,item=self.video)
        content2 = Content.objects.create(module=self.module, order=2, item=self.video)
        
        contents = Content.objects.all()
        self.assertEqual(contents[0], content2)
        self.assertEqual(contents[1], content1)

class TextModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='mohammad', password='testing4321')
    
    def test_can_save_and_retriving_objects(self):
        text_1 = Text.objects.create(title='this is text1', creator=self.user, text='text')

        self.assertIsNotNone(text_1)
        t_1 = Text.objects.first()
        self.assertEqual(text_1, t_1)

        text_2 = Text.objects.create(title='this is text2', creator=self.user, text='text')
        texts = Text.objects.all()
        self.assertEqual(texts.count(), 2)
        self.assertEqual(text_1.title, texts[0].title)
        self.assertEqual(text_2.title, texts[1].title)
    
    def test_text_render_to_text_template(self):
        text = Text.objects.create(title='this is text1', creator=self.user, text='text')
        self.assertIn('text', text.render())
        self.assertNotIn('image', text.render())
        self.assertNotIn('file', text.render())
        self.assertNotIn('video', text.render())

# class ImageModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='mohammad', password='testing4321')
    
#     def test_can_save_and_retriving_objects(self):
#         img = SimpleUploadedFile()
#         image_1 = Image.objects.create(title='this is image1', creator=self.user, image='default_image.jpg')

#         self.assertIsNotNone(text_1)
#         t_1 = Text.objects.first()
#         self.assertEqual(text_1, t_1)

#         text_2 = Text.objects.create(title='this is text2', creator=self.user, text='text')
#         texts = Text.objects.all()
#         self.assertEqual(texts.count(), 2)
#         self.assertEqual(text_1.title, texts[0].title)
#         self.assertEqual(text_2.title, texts[1].title)
    
#     def test_text_render_to_text_template(self):
#         text = Text.objects.create(title='this is text1', creator=self.user, text='text')
#         self.assertIn('text', text.render())
#         self.assertNotIn('image', text.render())
#         self.assertNotIn('file', text.render())
#         self.assertNotIn('video', text.render())

# class TextModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='mohammad', password='testing4321')
    
#     def test_can_save_and_retriving_objects(self):
#         text_1 = Text.objects.create(title='this is text1', creator=self.user, text='text')

#         self.assertIsNotNone(text_1)
#         t_1 = Text.objects.first()
#         self.assertEqual(text_1, t_1)

#         text_2 = Text.objects.create(title='this is text2', creator=self.user, text='text')
#         texts = Text.objects.all()
#         self.assertEqual(texts.count(), 2)
#         self.assertEqual(text_1.title, texts[0].title)
#         self.assertEqual(text_2.title, texts[1].title)
    
#     def test_text_render_to_text_template(self):
#         text = Text.objects.create(title='this is text1', creator=self.user, text='text')
#         self.assertIn('text', text.render())
#         self.assertNotIn('image', text.render())
#         self.assertNotIn('file', text.render())
#         self.assertNotIn('video', text.render())

# class TextModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='mohammad', password='testing4321')
    
#     def test_can_save_and_retriving_objects(self):
#         text_1 = Text.objects.create(title='this is text1', creator=self.user, text='text')

#         self.assertIsNotNone(text_1)
#         t_1 = Text.objects.first()
#         self.assertEqual(text_1, t_1)

#         text_2 = Text.objects.create(title='this is text2', creator=self.user, text='text')
#         texts = Text.objects.all()
#         self.assertEqual(texts.count(), 2)
#         self.assertEqual(text_1.title, texts[0].title)
#         self.assertEqual(text_2.title, texts[1].title)
    
#     def test_text_render_to_text_template(self):
#         text = Text.objects.create(title='this is text1', creator=self.user, text='text')
#         self.assertIn('text', text.render())
#         self.assertNotIn('image', text.render())
#         self.assertNotIn('file', text.render())
#         self.assertNotIn('video', text.render())


