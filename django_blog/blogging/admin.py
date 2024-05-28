from django.contrib import admin

from blogging.models import Post, Category

class CategoryInLine(admin.TabularInline):
    model = Category.posts.through
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [CategoryInLine]
    list_display = ('title', 'author', 'created_date', 'published_date')
    search_fields = ('title', 'text')
    list_filter = ('author', 'published_date')

class CategoryAdmin(admin.ModelAdmin):
    exclude = ('posts',)
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(Post)
admin.site.register(Category)