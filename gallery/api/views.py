from django.db.models import Count
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from gallery.api.permissions import CanListGalleryPhotos, CanViewGallery
from gallery.api.serializers import (
    GalleryLikeSerializer,
    GallerySerializer,
    PhotoLikeSerializer,
    PhotoSerializer,
)
from gallery.models import Gallery, Photo


class GalleryListCreateApiView(generics.ListCreateAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GalleryRetreiveApiView(generics.RetrieveAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [IsAuthenticated, CanViewGallery]


class GalleryLikeApiView(generics.RetrieveUpdateAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GalleryLikeSerializer
    permission_classes = [IsAuthenticated]


class PublicGalleryListApiView(generics.ListAPIView):
    queryset = Gallery.objects.filter(public=True)
    serializer_class = GallerySerializer
    permission_classes = [IsAuthenticated]


class PhotoListCreateApiView(generics.ListCreateAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated, CanListGalleryPhotos]

    def get_queryset(self):
        """
        list all photos related to a gallery given gallery_id
        """
        gallery_id = self.kwargs["gallery_id"]
        return Photo.objects.filter(gallery_id=gallery_id)


class PhotoLikeApiView(generics.RetrieveUpdateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoLikeSerializer
    permission_classes = [IsAuthenticated]


class TrendingPhotosListApiView(generics.ListAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        list all photos from public galleries where there number of likes is >= 2
        """
        return Photo.objects.annotate(likes_count=Count("likes")).filter(
            likes_count__gt=2, gallery__public=True
        )
