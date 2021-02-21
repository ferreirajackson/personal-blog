from django.db import models
from django.contrib.auth.models import User
"""Declare models for YOUR_APP app."""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField

# UserManager table
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

# User table
class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Newsletter(models.Model):
    email = models.CharField(max_length=255,null=True)
    status = models.CharField(max_length=10,null=True)

    def __str__(self):
        return str(self.email)

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255,null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
        # body = models.TextField()
    body = RichTextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
    'Category',
    on_delete=models.SET_NULL,
    null=True)
    categories = models.CharField(max_length=300,null=True)
    post_picture = models.ImageField(upload_to ='images/', null=True, blank=True)


    def __str__(self):
        return self.title+ ' | ' + str(self.author)


    @staticmethod
    def get_all_posts():
        return Post.objects.all()

    @staticmethod
    def get_all_posts_by_categoryid(category_name):
        if category_name:
            return Post.objects.filter(category = category_name)
        else:
            return Post.get_all_posts();


class Temp(models.Model):
    categories = models.CharField(max_length=300,null=True)


    def __str__(self):
        return str(self.categories)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    # def get_absolute_url(self):
    #     return reverse('post-category', kwargs={'pk': self.pk})

class Setup(models.Model):
    SetupKey = models.CharField(max_length=4,null=True)
    NumberPostsHome = models.IntegerField(null=True)


    def __str__(self):
        return str(self.NumberPostsHome)
