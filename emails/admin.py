from django.contrib import admin
from .models import EmailData


@admin.register(EmailData)
class EmailDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'comments', 'received_at')
    search_fields = ('name', 'comments')
    list_filter = ('received_at',)
    ordering = ('-received_at',)
