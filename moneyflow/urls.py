from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from ddsmgr.views import CategoryAutocomplete, SubcategoryAutocomplete


urlpatterns = [
    path("admin/", admin.site.urls),
    path("category-autocomplete/", CategoryAutocomplete.as_view(), name="category-autocomplete"),
    path("subcategory-autocomplete/", SubcategoryAutocomplete.as_view(), name="subcategory-autocomplete"),
    path("", lambda request: redirect("/admin/")),
]
