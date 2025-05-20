from django.db import models
from django.conf import settings


class Client(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('transito', 'Em Trânsito'),
        ('concluida', 'Concluída'),
    ]

    delivery_date = models.DateField(null=False, blank=False)
    departure_time = models.DateTimeField(null=True, blank=True)
    arrival_time = models.DateTimeField(null=True, blank=True)
    delivery_completed = models.DateTimeField(null=True, blank=True)
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, null=True, blank=False)
    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default='pendente')
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client.name

    def save(self, *args, **kwargs):
        if self.status == "pendente":
            self.driver = None
            self.arrival_time = None
            self.delivery_completed = None
            self.departure_time = None

        super().save(*args, **kwargs)
