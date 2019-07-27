from django.db import models
from django.conf.global_settings import AUTH_USER_MODEL

class SysUser(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    user = models.OneToOneField(AUTH_USER_MODEL, related_name='sys_user', on_delete=models.CASCADE)
    personal_image = models.ImageField(upload_to='admin/personal_image/', blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20, blank=True)

    def __str__(self):
        return self.user.get_full_name()


    
    
