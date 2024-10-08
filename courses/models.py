import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.text import slugify
from blogs.models import Author, Blog
from courses.managers import CustomUserManager
from teachers.models import Teacher


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    image = models.ImageField(upload_to='images/categories', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.slug:
            i = 1
            while True:
                new_slug = f"{slugify(self.title)}-{i}"
                if not Category.objects.filter(slug=new_slug).exists():
                    self.slug = new_slug
                    break
                i += 1

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Course(BaseModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    number_of_students = models.PositiveIntegerField(default=0)
    price = models.FloatField()
    duration = models.PositiveIntegerField()
    teachers = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos/courses')
    category = models.ForeignKey(Category, related_name='courses', on_delete=models.CASCADE, null=True, blank=True)

    @property
    def hours(self):
        if self.duration >= 60:
            hours = self.duration // 60
            return hours

    @property
    def minutes(self):
        if self.duration >= 60:
            minutes = self.duration % 60
            return minutes

    objects = models.Manager

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.slug:
            i = 1
            while True:
                new_slug = f"{slugify(self.title)}-{i}"
                if not Course.objects.filter(slug=new_slug).exists():
                    self.slug = new_slug
                    break
                i += 1

        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(BaseModel):
    class RatingChoices(models.TextChoices):
        Zero = '0'
        One = '1'
        Two = '2'
        Three = '3'
        Four = '4'
        Five = '5'

    name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    comment = models.TextField()
    media_file = models.FileField(upload_to='comments/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    rating = models.PositiveIntegerField(choices=RatingChoices.choices, default=RatingChoices.Zero.value)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_comments', blank=True,
                                  null=True)
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comments', blank=True, null=True)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_comments', blank=True,
                                   null=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=50)
    birth_of_date = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class BoughtCourse(BaseModel):
    name = models.CharField(max_length=50, blank=True, null=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='bought_courses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bought_courses')

    def __str__(self):
        return self.name


# models.py


class ContactMessage(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_token = models.UUIDField(default=uuid.uuid4, editable=False)

    objects = models.Manager
