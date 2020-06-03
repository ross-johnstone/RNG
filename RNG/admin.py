from django.contrib import admin
from RNG.models import UserProfile, Category, Game, Rating, Comment

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Game)
admin.site.register(Rating)
admin.site.register(Comment)
