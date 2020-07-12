from django.conf import settings
from django.db import models

from .utils import get_random_string

# Create your models here.


class Gallery(models.Model):
    """ Model for a gallery that includes photos.
        -name: name here is optional in case user want to just create a gallery.
        -user: user here is ForeignKey because user has many galleries and 
          a gallery belong to one user (one to many relation).
        -public: so that user can have private galleries in which he only have access to them.
        -likes: likes is ManyToManyField to create new model of gallery and user
         to be able to track who liked the gallery and if user liked the gallery before or not.
    """

    # gallery owner
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # gallery name is optional
    name = models.CharField(max_length=250, null=True, blank=True)
    public = models.BooleanField(default=True, db_index=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_galleries"
    )

    @property
    def number_of_likes(self):
        return self.likes.count()


def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/gallery/<Gallery_id>/random str/<filename>
    # random string is used here to prevent file overwrite with same <filename>
    return "gallery/{0}/{1}/{2}".format(
        instance.gallery.id, get_random_string(5), filename
    )


class Photo(models.Model):
    """ Model for adding photos in a gallery. 
        -gallery: gallery here is ForeignKey because gallery includes many photos and 
         a photo belong to one gallery (one to many relation).
        -description: description is TextField to allow large text.
        -image: image is ImageField because it handels uploading the file using upload_to kwarg 
         and saves its path.
        -likes: likes is ManyToManyField to create new model of photo and user
         to be able to track who liked the photo and if user liked the photo before or not.
        
    """

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
