import datetime
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField

def getFileName(request, filename):
    return os.path.join('Images/', filename)

def getlogo(request, filename):
    now_time = datetime.datetime.now().strftime('%Y%m%d%X')
    new_filename = "{}{}".format(now_time, filename)
    return os.path.join('logo/', new_filename)

def picture(request, filename):
    now_time = datetime.datetime.now().strftime('%Y%m%d%X')
    new_filename = "{}{}".format(now_time, filename)
    return os.path.join('picture/', new_filename)

def video(request, filename):
    now_time = datetime.datetime.now().strftime('%Y%m%d%X')
    new_filename = "{}{}".format(now_time, filename)
    return os.path.join('video/', new_filename)

def blog_images(request, filename):
    now_time = datetime.datetime.now().strftime('%Y%m%d%X')
    new_filename = "{}{}".format(now_time, filename)
    return os.path.join('media/', new_filename)

class AdminLoginManager(BaseUserManager):
    def create_user(self, username, email, ph_no, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            ph_no=ph_no,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, ph_no, password=None):
        user = self.create_user(
            email=email,
            username=username,
            ph_no=ph_no,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class AdminLogin(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    ph_no = PhoneNumberField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = AdminLoginManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'ph_no']

    def __str__(self):
        return self.username

class Course(models.Model):
    Title = models.CharField(max_length=100)
    Description = RichTextField()
    Technologies = models.CharField(max_length=150)
    Images = models.ImageField(upload_to=getFileName, blank=False)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True, blank=True)
    modified_by = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

class Technology(models.Model):
    Technologies = models.CharField(max_length=150)

class PartnerLogo(models.Model):
    name = models.CharField(max_length=100, default=None)
    logo = models.ImageField(upload_to=getlogo)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True, blank=True)
    modified_by = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

class Testimonial(models.Model):
    student_name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=picture, blank=False)
    course = models.CharField(max_length=100)
    date = models.DateField()
    testimonial = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True, blank=True)
    modified_by = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

class PlacementStory(models.Model):
    student_name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    testimonial_video = models.FileField(upload_to=video, blank=False)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True, blank=True)
    modified_by = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True, blank=True)
    modified_by = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

class Blog(models.Model):
    images = models.ImageField(upload_to=blog_images, blank=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    course = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True, blank=True)
    modified_by = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

class Career(models.Model):
    Logo = models.ImageField(upload_to=getlogo, blank=False)
    Job_Heading = models.CharField(max_length=100)
    Location = models.CharField(max_length=100)
    Experience = models.CharField(max_length=100)
    No_Of_Openings = models.CharField(max_length=100)
    Salary = models.FloatField()
    Status = models.BooleanField(default=True)
    Job_Type = models.CharField(max_length=100)
    Qualification = models.CharField(max_length=255)
    Job_Description = models.TextField()
    Skills_Required = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True, blank=True)
    modified_by = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
