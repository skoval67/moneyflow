from django import forms
from .models import Transaction, Subcategory
from django.core.exceptions import ValidationError
from dal import autocomplete


class TransactionForm(forms.ModelForm):
    created_at = forms.DateField(
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
    )

    class Meta:
        model = Transaction
        fields = ["status", "type", "category", "subcategory", "amount", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 2}),
            "category": autocomplete.ModelSelect2(url="category-autocomplete", forward=["type"], ),
            "subcategory": autocomplete.ModelSelect2(url="subcategory-autocomplete", forward=["category"], )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # "amount", "type", "category" и "subcategory" обязательны → django сам пометит required по модели.
        # По умолчанию оставляем подбор subcategory пустым (пока не выбрана category)
        self.fields["subcategory"].queryset = Subcategory.objects.none()

        # если пришли данные (редактирование или POST с выбранной category), наполняем подкатегории
        data = self.data or self.initial
        category_id = None
        if data.get("category"):
            category_id = data.get("category")
        elif self.instance and self.instance.pk:
            category_id = getattr(self.instance.category, "pk", None)
        if category_id:
            self.fields["subcategory"].queryset = Subcategory.objects.filter(category_id=category_id)

    def clean(self):
        cleaned = super().clean()
        category = cleaned.get("category")
        typ = cleaned.get("type")
        subcat = cleaned.get("subcategory")

        if not category or not typ or not subcat:
            # fields required check will handle missing, but keep explicit error messages
            raise ValidationError("Поля 'тип', 'категория' и 'подкатегория' обязательны.")

        if category.type_id != typ.id:
            raise ValidationError("Выбранная категория не принадлежит выбранному типу.")

        if subcat.category_id != category.id:
            raise ValidationError("Выбранная подкатегория не принадлежит выбранной категории.")

        return cleaned
