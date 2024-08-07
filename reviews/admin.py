from django.contrib import admin
from .models import Review

# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'review_text')
    readonly_fields = ('user', 'order', 'review_text')

    # Remove editing options from the admin interface
    def has_change_permission(self, request, obj=None):
        return False 


admin.site.register(Review, ReviewAdmin)