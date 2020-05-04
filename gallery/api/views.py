from django.db.models import Count
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from gallery.api.permissions import (
    CanCreateGalleryPhoto,
    CanListGalleryPhotos,
    CanViewGallery,
)
from gallery.api.serializers import (
    GalleryLikeSerializer,
    GallerySerializer,
    PhotoLikeSerializer,
    PhotoSerializer,
)
from gallery.models import Gallery, Photo


class GalleryListCreateApiView(generics.ListCreateAPIView):
    """ Create and list galleries """

    queryset = Gallery.objects.annotate(likes_count=Count("likes")).all()
    serializer_class = GallerySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GalleryRetreiveApiView(generics.RetrieveAPIView):
    """ Get a gallery by id.
        Any user can view public gallaries.
        Only the gallery owner can view it if it is private.
    """

    queryset = Gallery.objects.annotate(likes_count=Count("likes")).all()
    serializer_class = GallerySerializer
    permission_classes = [IsAuthenticated, CanViewGallery]


class GalleryLikeApiView(generics.RetrieveUpdateAPIView):
    """ Like a gallery given gallery id.
        Getting the user from the request inside the serializer.
    """

    queryset = Gallery.objects.all()
    serializer_class = GalleryLikeSerializer
    permission_classes = [IsAuthenticated]


class PublicGalleryListApiView(generics.ListAPIView):
    """ List public galleries """

    queryset = Gallery.objects.annotate(likes_count=Count("likes")).filter(public=True)
    serializer_class = GallerySerializer
    permission_classes = [IsAuthenticated]


class PhotoListCreateApiView(generics.ListCreateAPIView):
    """ List and create photos.
        Any user can list photos of a public gallary.
        Only the gallery owner can list its photos if it is private.
    """

    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated, CanListGalleryPhotos, CanCreateGalleryPhoto]

    def get_queryset(self):
        """
        list all photos related to a gallery given gallery_id
        """
        gallery_id = self.kwargs["gallery_id"]
        return Photo.objects.annotate(likes_count=Count("likes")).filter(
            gallery_id=gallery_id
        )


class PhotoLikeApiView(generics.RetrieveUpdateAPIView):
    """ Like photo given photo id.
        Getting the user from the request inside the serializer.
    """

    queryset = Photo.objects.all()
    serializer_class = PhotoLikeSerializer
    permission_classes = [IsAuthenticated]


class TrendingPhotosListApiView(generics.ListAPIView):
    """ List Trending Photos based on number of likes of the photos from 
        public galleries only.
    """

    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        list all photos from public galleries where there number of likes is >= 2
        """
        return Photo.objects.annotate(likes_count=Count("likes")).filter(
            likes_count__gt=2, gallery__public=True
        )
