from django.contrib import admin

# Register your models here.
from .models import Post, Category, Tag, Comment, Bookmark


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'category', 'created_on', 'status')
    list_filter = ('status', 'category')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'content', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ['user__username', 'content']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_on')
    list_filter = ('created_on',)
    search_fields = ['user__username', 'post__title']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bookmark, BookmarkAdmin)

