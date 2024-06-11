from django.db import models

NULLABLE = {"null": True, "blank": True}


class Client(models.Model):
    """Модель для клента"""

    email = models.EmailField(verbose_name="Контактный email", unique=True)
    name = models.CharField(max_length=100, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий", **NULLABLE)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.email
