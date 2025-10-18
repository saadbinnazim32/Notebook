from django.contrib import admin
from .models import Message,User

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('text', 'created_at')

# Custom user admin to show messages inline
class CustomUserAdmin(admin.ModelAdmin):
    inlines = [MessageInline]

# Unregister default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Separate Message admin with filter by user
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at')
    list_filter = ('user', 'created_at')       # This adds filter sidebar
    search_fields = ('text', 'user__username')

admin.site.register(Message, MessageAdmin)

# class MessageAdmin(admin.ModelAdmin):
#     list_display = ('user', 'text', 'created_at')  # columns to show
#     list_filter = ('user', 'created_at')           # this adds the filter sidebar
#     search_fields = ('text', 'user__username')     # optional: search box



# admin.site.register(Message)

# Register your models here.
