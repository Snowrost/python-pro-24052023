import uuid

from django.db import models

from .dealer import Dealer


class Warehouse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} – {self.id}"
