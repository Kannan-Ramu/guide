from django.contrib import admin
from .models import Comment
from import_export.admin import ImportExportModelAdmin
from import_export import resources
# Register your models here.

class CommentsResource(resources.ModelResource):
    class Meta:
        model = Comment
        fields = ('teamID', 'guide', 'guide_email', 'body', 'published_date')


class CommentsAdmin(ImportExportModelAdmin):
    list_display = ('teamID', 'guide', 'guide_email', 'body', 'published_date')
    ordering = ('teamID',)
    search_fields = ('teamID', 'guide', 'guide_email')
    resource_class = CommentsResource

admin.site.register(Comment, CommentsAdmin)
