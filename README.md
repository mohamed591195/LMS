# LMS
#### To Use the project 
1) Make a virtual env beside the cloned repositry and activate it
2) just install project dependedcies 

   `` pip install -r requirments.txt ``
  
 3) run this command to start the project by dev server
 
   `` python manage.py runserver `` 
   
 4) you can access it locally from ``localhost:8000`` or ``127.0.0.1:8000``
 
 5) create a superuser account to log into admin panel so you can control the site by this command
  `` python manage.py createsuperuser ``
 6) rerun the dev server again and access the admin path within the host ``loclhost:8000`` 
 
 ### the site has four different types of users
 1) **superuser**\
    who wil have access to the panel of the site and have all permissions
 2) ** site admins**\
    these will be a normal users with admin privilege, the will belong to ``Admins`` group which gives them their privileges
   
 3) **Instructors**\
    one of the admins responsibility is to add instructors and instructors is just a normal user with instructors privileges\
    they belong to ``Instructors`` group 
    
 4) **Normal User**\
    they are the realusers of the site not and have no administration responsibilities \
    they don't belong to any group and have no permissions to edit any data
    , they have the ability to enroll in courses and contribute to discussions and vote up comments, etc.
    
    
