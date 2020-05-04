from django.contrib.auth import get_user_model
from django.db.models import Count
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from gallery.api.serializers import GallerySerializer
from gallery.models import Gallery

User = get_user_model()


class GalleryTests(APITestCase):
    """ Test only gallery apis """

    def setUp(self):
        self.user1 = self.create_user("user1", "user1@test.com")
        self.user2 = self.create_user("user2", "user2@test.com")

    def create_user(self, username, email):
        return User.objects.create(username=username, email=email)

    def test_list_galleries(self):
        """
        Assert galleries are listed successfully.
        """
        url = reverse("gallery:api_gallery:list_create_galleries")
        gallery1 = Gallery.objects.create(name="gallery1", user=self.user1)
        gallery2 = Gallery.objects.create(name="gallery2", user=self.user1)
        self.client.force_login(self.user1)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        list = Gallery.objects.annotate(likes_count=Count("likes"))
        self.assertEqual(
            response.data["results"][0], GallerySerializer(list[0]).data,
        )
        self.assertEqual(
            response.data["results"][1], GallerySerializer(list[1]).data,
        )

    def test_list_galleries_auth_and_perm(self):
        """ Assert api can only be accessed by authenticated users 
            Assert api can be accessed by any authenticated user.
        """
        url = reverse("gallery:api_gallery:list_create_galleries")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_login(self.user1)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_public_galleries(self):
        """
        Assert public galleries are listed successfully and no private ones included.
        """
        url = reverse("gallery:api_gallery:list_public_galleries")
        gallery1 = Gallery.objects.create(name="gallery1", user=self.user1)
        gallery2 = Gallery.objects.create(
            name="gallery2", user=self.user1, public=False
        )
        list = Gallery.objects.annotate(likes_count=Count("likes")).filter(public=True)
        self.client.force_login(self.user1)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0], GallerySerializer(list[0]).data,
        )

    def test_list_public_galleries_auth_and_perm(self):
        """ Assert api can only be accessed by authenticated users 
            Assert api can be accessed by any authenticated user.
        """
        url = reverse("gallery:api_gallery:list_public_galleries")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_login(self.user1)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retreive_gallery(self):
        """
        Assert that a gallery can be retreived successfully either it is public or private.
        """

        gallery1 = Gallery.objects.create(name="gallery1", user=self.user1)
        gallery2 = Gallery.objects.create(
            name="gallery2", user=self.user1, public=False
        )
        list = Gallery.objects.annotate(likes_count=Count("likes"))
        url1 = reverse("gallery:api_gallery:get_gallery", args=[gallery1.id])
        url2 = reverse("gallery:api_gallery:get_gallery", args=[gallery2.id])
        self.client.force_login(self.user1)
        response = self.client.get(url1, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, GallerySerializer(list.filter(id=gallery1.id).first()).data,
        )
        response = self.client.get(url2, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, GallerySerializer(list.filter(id=gallery2.id).first()).data,
        )

    def test_retreive_gallery_auth_and_perm(self):
        """
        Assert that a gallery can't be retreived:
            if user is not authenticated.
            if gallery is private and auth user is not the owner.
        Assert only owner can access his private gallery.
        """

        gallery_public = Gallery.objects.create(name="gallery1", user=self.user1)
        gallery_private = Gallery.objects.create(
            name="gallery2", user=self.user1, public=False
        )
        list = Gallery.objects.annotate(likes_count=Count("likes"))
        url1 = reverse("gallery:api_gallery:get_gallery", args=[gallery_public.id])
        url2 = reverse("gallery:api_gallery:get_gallery", args=[gallery_private.id])
        # test authentication
        response = self.client.get(url1, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # test permissions
        # user2 (not owner) can access the gallery because it is public
        self.client.force_login(self.user2)
        response = self.client.get(url1, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            GallerySerializer(list.filter(id=gallery_public.id).first()).data,
        )
        # user2 (not owner) can't access the gallery because it is private
        response = self.client.get(url2, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # user1 (owner) can access his private gallery
        self.client.force_login(self.user1)
        response = self.client.get(url2, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_gallery(self):
        """
        Assert gallery is created successfully.
        Assert gallery.user is the authenticated user.
        Assert gallery.name is optional.
        Assert gallery.public is optional with default=True.
        """
        url = reverse("gallery:api_gallery:list_create_galleries")
        data = {"name": "gallery1"}
        self.client.force_login(self.user1)
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Gallery.objects.count(), 1)
        self.assertEqual(Gallery.objects.first().name, data["name"])
        self.assertEqual(Gallery.objects.first().user, self.user1)

        data = {"public": False}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Gallery.objects.count(), 2)
        self.assertEqual(Gallery.objects.last().name, None)
        self.assertEqual(Gallery.objects.last().user, self.user1)
        self.assertEqual(Gallery.objects.last().public, data["public"])

    def test_create_gallery_auth_and_perm(self):
        """
        Assert that only auth users can create a gallery.
        """
        url = reverse("gallery:api_gallery:list_create_galleries")
        data = {}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_login(self.user1)
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_like_gallery(self):
        """
        Assert gallery likes increase when liked.
        Assert user who likes exist in gallery.likes many to many table.
        Assert user who likes is added to gallery.likes without affecting other likes.
        Assert liking more than once has no effect.
        """
        gallery = Gallery.objects.create(name="gallery1", user=self.user1)
        url = reverse("gallery:api_gallery:like_gallery", args=[gallery.id])
        data = {}
        self.assertEqual(gallery.number_of_likes, 0)
        self.client.force_login(self.user1)
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(gallery.number_of_likes, 1)
        self.assertTrue(gallery.likes.filter(id=self.user1.id).exists())
        # liking again with same user doesn't change anything
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(gallery.number_of_likes, 1)
        # test like with different user
        self.client.force_login(self.user2)
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(gallery.number_of_likes, 2)
        self.assertTrue(
            gallery.likes.filter(id__in=[self.user1.id, self.user2.id]).exists()
        )

    def test_like_gallery_auth_and_perm(self):
        """
        Assert any auth user can like a gallery(public or private) and non auth user can't.
        """
        gallery = Gallery.objects.create(name="gallery1", user=self.user1)
        url = reverse("gallery:api_gallery:like_gallery", args=[gallery.id])
        data = {}
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_login(self.user1)
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test public gallery can be liked by a non owner
        self.client.force_login(self.user2)
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test private gallery can be liked by a non owner
        gallery.public = False
        gallery.save()
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
