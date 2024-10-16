from django.db import models
from django.contrib.auth.models import User

#! Post Model
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)  # Changed integer to boolean
    # image = models.CharField(max_length=255, null=True, blank=True)  
    image = models.FileField(upload_to='post_images/',null=True, blank=True)
    category_set = models.ManyToManyField('app_thaisweets.Category')
    
    def __str__(self):
        return self.title

#! Category Model
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

#! Comment Model
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

#! Share Model
class Share(models.Model):
    share_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
    count = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Share by {self.user.username} on Post {self.post.title}"

# ! UserProfille model
class Userprofile(models.Model):
    age = models.IntegerField(null=True, blank=True)
    image = models.FileField(upload_to='profile_images/',null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)