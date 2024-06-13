from django.conf import settings
from django.db import models

NULLABLE = {"null": True, "blank": True}


class Client(models.Model):
    """Модель для клента"""

    email = models.EmailField(verbose_name="Контактный email", unique=True)
    name = models.CharField(max_length=100, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий", **NULLABLE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,
        on_delete=models.CASCADE,
        related_name="clients",
        verbose_name="Автор",
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.email
