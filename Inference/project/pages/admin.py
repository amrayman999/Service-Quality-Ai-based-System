from django.contrib import admin
from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('Subject','review','Sector' , 'Governorate','City', 'Important_Topics','Sentiment_type', 'Topic', 'Recommended_action' )
    
admin.site.register(Review , ReviewAdmin)
admin.site.site_header = "Admin Page"
admin.site.site_title = "Admin Page"
# Register your models here.
