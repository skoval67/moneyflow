# from django.shortcuts import render
from dal import autocomplete
from .models import Category, Subcategory


class SubcategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Subcategory.objects.all()

        category_id = self.forwarded.get("category")
        if category_id:
            qs = qs.filter(category_id=category_id)

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs
    
class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Category.objects.all()

        type_id = self.forwarded.get("type")
        if type_id:
            qs = qs.filter(type_id=type_id)

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

