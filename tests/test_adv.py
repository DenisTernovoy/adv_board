from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from adv.models import Advertisement, Review
from users.models import CustomUser


class TestAdv(APITestCase):
    """Тестирование приложения adv"""

    def setUp(self) -> None:
        self.user = CustomUser.objects.create(
            first_name="Test",
            last_name="User",
            email="test@test.com",
        )
        self.user.set_password("12345678")
        self.user.save()

        data_advertisement = {
            "title": "Машинка",
            "price": 1500,
            "description": "Игрушка",
            "author": self.user,
        }

        self.advertisement = Advertisement.objects.create(**data_advertisement)
        self.advertisement.save()

        data_review = {
            "text": "Неплохая игрушка",
            "ad": self.advertisement,
            "author": self.user,
        }

        self.review = Review.objects.create(**data_review)
        self.review.save()

        self.client.force_authenticate(self.user)

    def test_create_advertisement(self):
        """Тестирование контроллера создания объявления"""

        url = reverse("adv:advertisement-list")

        data = {"title": "Кукла", "price": 2000, "description": "Игрушка"}

        response_ok = self.client.post(url, data)

        adv = Advertisement.objects.get(title="Кукла")

        self.assertEqual(str(adv), f"{data['title']} - {data['price']}")
        self.assertEqual(response_ok.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Advertisement.objects.count(), 2)
        self.assertEqual(response_ok.json()["title"], data["title"])
        response_nok = self.client.post(url, data, format="json")
        self.assertEqual(response_nok.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_advertisement(self):
        """Тестирование контроллера обновления объявления"""

        url = reverse("adv:advertisement-detail", args=(self.advertisement.pk,))

        data = {"title": "Машинка", "price": 2500, "description": "Игрушка"}

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Advertisement.objects.get(pk=self.advertisement.pk).price, data["price"]
        )

    def test_retrieve_advertisement(self):
        """Тестирование контроллера получения одного объявления"""

        url = reverse("adv:advertisement-detail", args=(self.advertisement.pk,))

        response = self.client.get(url)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result["title"], self.advertisement.title)
        self.assertEqual(result["price"], self.advertisement.price)
        self.assertEqual(result["description"], self.advertisement.description)

    def test_destroy_advertisement(self):
        """Тестирование контроллера удаления объявления"""

        url = reverse("adv:advertisement-detail", args=(self.advertisement.pk,))

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_advertisement(self):
        """Тестирование контроллера получения списка объявлений"""

        url = reverse("adv:advertisement-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_review(self):
        """Тестирование контроллера создания отзыва"""

        url = reverse("adv:reviews-list", kwargs={"ad_pk": self.advertisement.pk})

        data = {"text": "Мне понравилась игрушка"}

        response_ok = self.client.post(url, data)
        self.assertEqual(response_ok.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        self.assertEqual(response_ok.json()["text"], data["text"])
        response_nok = self.client.post(url, data, format="json")
        self.assertEqual(response_nok.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_review(self):
        """Тестирование контроллера обновления отзыва"""

        url = reverse(
            "adv:reviews-detail",
            kwargs={"pk": self.review.pk, "ad_pk": self.advertisement.pk},
        )

        data = {
            "text": "Неплохая игрушка. Детям понравилась!",
        }

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.get(pk=self.review.pk).text, data["text"])

    def test_retrieve_review(self):
        """Тестирование контроллера получения одного отзыва"""

        url = reverse(
            "adv:reviews-detail",
            kwargs={"pk": self.review.pk, "ad_pk": self.advertisement.pk},
        )

        response = self.client.get(url)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result["text"], str(self.review))
        self.assertEqual(result["author"], self.user.pk)

    def test_destroy_review(self):
        """Тестирование контроллера удаления отзыва"""

        url = reverse(
            "adv:reviews-detail",
            kwargs={"pk": self.review.pk, "ad_pk": self.advertisement.pk},
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_review(self):
        """Тестирование контроллера получения списка отзывов"""

        url = reverse("adv:reviews-list", kwargs={"ad_pk": self.advertisement.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
