from django.contrib import admin
from .models import OfferingCategory, Offering, SiteSettings


@admin.register(OfferingCategory)
class OfferingCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Offering)
class OfferingAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'category',
        'amount',
        'payment_method',
        'service_date',
        'created_by'
    ]

    list_filter = [
        'payment_method',
        'service_date',
        'category'
    ]

    search_fields = [
        'category__name',
        'remarks'
    ]

    # 🔥 AUTO SAVE LOGGED-IN USER
    def save_model(self, request, obj, form, change):

        if not obj.created_by:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)


admin.site.register(SiteSettings)