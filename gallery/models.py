from django.conf import settings
from django.db import models

from .utils import get_random_string

# Create your models here.


class Gallery(models.Model):
    # gallery owner
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # gallery name is optional
    name = models.CharField(max_length=250, null=True, blank=True)
    public = models.BooleanField(default=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_galleries"
    )

    @property
    def number_of_likes(self):
        return self.likes.count()


def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/gallery/<Gallery_id>/random str/<filename>
    return "gallery/{0}/{1}/{2}".format(
        instance.gallery.id, get_random_string(5), filename
    )


class Photo(models.Model):
    gallery = models.ForeignKey("gallery.Gallery", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(upload_to=image_directory_path)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_photos"
    )

    @property
    def number_of_likes(self):
        return self.likes.count()
