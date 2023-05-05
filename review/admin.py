from django.contrib import admin
from .models import Ticket, Review, UserFollows


class TicketAdmin(admin.ModelAdmin):
    """Admin for the ticket"""

    list_display = ("id", "title", "description", "user", "image")
    list_filter = ("user",)


class ReviewAdmin(admin.ModelAdmin):
    """Admin for the Review"""

    list_display = ("id", "headline", "body", "user", "rating", "ticket")
    list_filter = ("user",)


# Register your models here.
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows)
