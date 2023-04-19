from django.contrib import admin
from .models import BestTeam
from import_export.admin import ImportExportModelAdmin
from import_export import resources
# Register your models here.


class BestTeamResource(resources.ModelResource):
    class Meta:
        model = BestTeam
        fields = ('id', 'teamID',)


class BestTeamAdmin(ImportExportModelAdmin):
    list_display = ('teamID',)
    ordering = ('teamID',)
    search_fields = ('teamID',)
    resource_class = BestTeamResource


admin.site.register(BestTeam, BestTeamAdmin)
