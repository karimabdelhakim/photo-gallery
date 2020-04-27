from django.urls import path

from gallery.api import views

app_name = "gallery_api"

urlpatterns = [
    path(
        "galleries/",
        view=views.GalleryListCreateApiView.as_view(),
        name="list_create_galleries",
    ),
    path(
        "galleries/<int:pk>",
        view=views.GalleryRetreiveApiView.as_view(),
        name="get_gallery",
    ),
    path(
        "galleries/<int:pk>/like/",
        view=views.GalleryLikeApiView.as_view(),
        name="like_gallery",
    ),
    path(
        "galleries/public/",
        view=views.PublicGalleryListApiView.as_view(),
        name="list_public_galleries",
    ),
    path(
        "galleries/<int:gallery_id>/photos/",
        view=views.PhotoListCreateApiView.as_view(),
        name="list_create_photos",
    ),
    path(
        "photos/<int:pk>/like/",
        view=views.PhotoLikeApiView.as_view(),
        name="like_photo",
    ),
    path(
        "photos/trending/",
        view=views.TrendingPhotosListApiView.as_view(),
        name="list_trending_photos",
    ),
]
