from django.db import models
from django.utils.text import slugify
from django.conf import settings

class Post(models.Model):
   title = models.CharField(max_length=200, unique=True)
   image = models.ImageField(upload_to="posts/", null=True, blank=True, max_length=500)
   slug = models.SlugField(max_length=220, unique=True, blank=True)
   content = models.TextField()
   author = models.ForeignKey(
       settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True, blank=True,
       related_name="posts",)#related names for view
   created_at = models.DateTimeField(auto_now_add=True)
   def __str__(self):
       return self.title
   def save(self, *args, **kwargs):
       if not self.slug:
           self.slug = slugify(self.title)
       super().save(*args, **kwargs)
   def total_likes(self):
       return self.likes.count()

   def total_dislikes(self):
       return self.dislikes.count()


class Message(models.Model):
   post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="messages")
   sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
   recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages")
   body = models.TextField(max_length=2000)
   is_read = models.BooleanField(default=False)
   created_at = models.DateTimeField(auto_now_add=True)

   class Meta:
       ordering = ["created_at"]

   def __str__(self):
       return f"Message from {self.sender} about {self.post}"
