from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
import uuid
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)  # Explicitly define username
    phone_number = models.CharField(max_length=15, unique=True)

    birthdate = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    objects = CustomUserManager() 

    USERNAME_FIELD = "email"  # Authenticate using email
    REQUIRED_FIELDS = ["username", "phone_number"]  # Only these are required when creating a user

    def __str__(self):
        return self.email


class Post(models.Model):
    owner = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,related_name='my_posts')
    title = models.CharField(max_length=50)
    description  = models.TextField(null=True,blank=True)
    posted_at = models.DateTimeField( auto_now_add= True )
    image = models.ImageField(upload_to='posts',default='image.png')

  

    def __str__(self):
        return f'post {self.title} - {self.posted_at}'
    