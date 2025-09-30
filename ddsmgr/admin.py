from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from rangefilter.filters import DateRangeFilter
from .models import Status, Type, Category, Subcategory, Transaction
from .forms import TransactionForm
# from django.utils.html import format_html
from django.utils import timezone


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    # inlines = [SubcategoryInline]

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category__name", "category")
    search_fields = ("name",)

    def category_type(self, obj):
        return obj.category.type.name if obj.category else "-"
    category_type.short_description = "Тип"

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    form = TransactionForm
    list_display = ("created_at", "status", "type", "category", "subcategory", "amount", "short_comment")
    list_filter = ("status", "type", "category", "subcategory", ("created_at", DateRangeFilter))
    search_fields = ("comment",)
    date_hierarchy = "created_at"
    # change_list_template = "admin/ddsmgr/transaction_change_list.html"  # optional customizations

    def short_comment(self, obj):
        return obj.comment[:60] if obj.comment else "-"
    short_comment.short_description = "Комментарий"

    class Media:
        js = ("admin/ddsmgr/transaction_admin.js",)  # мы подключаем JS для динамики

    # Админ-view для AJAX: вернуть список подкатегорий по category_id
    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('get_subcategories/', self.admin_site.admin_view(self.get_subcategories), name="ddsmgr_get_subcategories"),
        ]
        return custom + urls

    def get_subcategories(self, request):
        category_id = request.GET.get("category")
        from django.core import serializers
        if not category_id:
            return JsonResponse({"results": []})
        subs = Subcategory.objects.filter(category_id=category_id).values("id", "name")
        return JsonResponse({"results": list(subs)})

    def get_changeform_initial_data(self, request):
        return {
            "created_at": timezone.now().date()  # ← подставляем дату в форму
        }
