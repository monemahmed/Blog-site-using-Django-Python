from django.contrib import admin
from .models import Post, Comment

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish', 'status')
    list_filter = ('status', 'author', 'publish', 'created')
    search_fields = ('body', 'title', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'mail', 'created', 'active')
    list_filter = ('active', 'created', 'post')
    search_fields = ('name', 'mail', 'body')


admin.site.register(Comment, CommentAdmin)
