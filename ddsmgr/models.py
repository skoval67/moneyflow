from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=150)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="categories")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")

    class Meta:
        unique_together = ("name", "category")
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return self.name

class Transaction(models.Model):
    created_at = models.DateField(default=timezone.now, verbose_name="Дата создания")  # auto set, but editable in forms
    # allow manual editing in admin via form
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="transactions", verbose_name="Статус")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, related_name="transactions", verbose_name="Тип")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="transactions", verbose_name="Категория")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, related_name="transactions", verbose_name="Подкатегория")
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Сумма")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.created_at} | {self.type} | {self.amount}₽"

    def clean(self):
        # дополнительная логика проверки целостности связей
        from django.core.exceptions import ValidationError
        if self.subcategory and self.category and self.subcategory.category_id != self.category_id:
            raise ValidationError("Выбранная подкатегория не относится к выбранной категории.")
