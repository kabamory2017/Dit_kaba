from django.contrib import admin
from .models import Post,Comment,LikeDislike

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("content","image","created_at" )

admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
admin.site.register(LikeDislike)


