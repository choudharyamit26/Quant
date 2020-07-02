from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    content = RichTextField(default='content')

    # Image = RichTextUploadingField(null=True,blank=True)

    def get_absolute_url(self):
        return reverse("adminpanel:post-detail", kwargs={'pk': self.pk})
