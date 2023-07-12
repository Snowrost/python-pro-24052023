import uuid

from django.contrib.auth.models import Permission, User
from django.urls import reverse
from faker import Faker
from faker.providers import address, company, person, profile
from rest_framework.test import APITestCase

from stock.models import Dealer, Warehouse

FAKE = Faker()
FAKE.add_provider(person)
FAKE.add_provider(company)
FAKE.add_provider(profile)
FAKE.add_provider(address)


class WarehousesTest(APITestCase):
    def test_list_warehouses(self):
        # given
        user = User.objects.create_user(
            FAKE.simple_profile()["username"],
            password="test",
            first_name=FAKE.first_name(),
            last_name=FAKE.last_name(),
        )
        dealer = Dealer.objects.create(owner=user, name=FAKE.company())
        warehouse = Warehouse.objects.create(name=FAKE.street_address(), dealer=dealer)
        url = reverse("warehouses-list")

        expected_result = [
            {
                "id": str(warehouse.id),
                "name": warehouse.name,
                "dealer": {
                    "id": str(dealer.id),
                    "name": dealer.name,
                    "owner": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                },
            }
        ]

        # when
        response = self.client.get(url).json()

        # then
        self.assertEquals(
            response,
            expected_result,
        )

    def test_create_warehouse(self):
        # given
        user = User.objects.create_user(
            FAKE.simple_profile()["username"],
            password="test",
            first_name=FAKE.first_name(),
            last_name=FAKE.last_name(),
        )
        permissions = Permission.objects.all()
        user.user_permissions.set(permissions)
        dealer = Dealer.objects.create(owner=user, name=FAKE.company())
        url = reverse("warehouses-list")
        warehouse_name = FAKE.street_address()

        self.client.login(username=user.username, password="test")

        # when
        response = self.client.post(
            url, data={"name": warehouse_name, "dealer": dealer.id}
        ).json()

        # then
        self.assertEquals(response["name"], warehouse_name)
        self.assertEquals(response["dealer"]["id"], str(dealer.id))
        self.assertEquals(response["dealer"]["name"], dealer.name)
        self.assertEquals(
            response["dealer"]["owner"],
            {"id": user.id, "first_name": user.first_name, "last_name": user.last_name},
        )

        # and
        saved_warehouse = Warehouse.objects.get(pk=response["id"])
        self.assertEquals(saved_warehouse.name, warehouse_name)
        self.assertEquals(saved_warehouse.dealer, dealer)

        # Tear down
        self.client.logout()
