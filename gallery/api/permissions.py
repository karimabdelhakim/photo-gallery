from django.shortcuts import get_object_or_404
from rest_framework import permissions

from gallery.models import Gallery


class CanViewGallery(permissions.BasePermission):
    """
    Any user can view the gallery if it is public.
    Only gallery owner can view a private gallery
    """

    message = "This gallery is private"

    def has_object_permission(self, request, view, obj):
        if request.method != "GET" or obj.public:
            return True
        return obj.user == request.user


class CanListGalleryPhotos(permissions.BasePermission):
    """
    Any user can view the gallery if it is public.
    Only gallery owner can view a private gallery
    """

    message = "This gallery is private"

    def has_permission(self, request, view):
        gallery = get_object_or_404(Gallery, pk=view.kwargs.get("gallery_id"))
        if request.method != "GET" or gallery.public:
            return True
        return gallery.user == request.user


class CanCreateGalleryPhoto(permissions.BasePermission):
    """
    Only gallery owner can add a photo to his gallery
    """

    message = "You don't have permission to add a photo to this gallery"

    def has_permission(self, request, view):
        if request.method != "POST":
            return True
        gallery = get_object_or_404(Gallery, pk=view.kwargs.get("gallery_id"))
        return gallery.user == request.user
