from django.contrib import admin
from .models import Client, PlaceOfWork, Interest, Target, Campaign, Message, JobType, EventsLog, FeedbacksType, FeedbacksLog, FeedbacksCategory
from .models import PlaceOfWorkCopy, InterestCopy, TargetCopy, JobTypeCopy

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'contact_phone', 'address', 'created_at', 'updated_at', 'id')
    search_fields = ('name', 'email')

@admin.register(PlaceOfWork)
class PlaceOfWorkAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'address', 'id')
    list_filter = ('client',)
    search_fields = ('name',)

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'id')
    list_filter = ('client',)
    search_fields = ('name',)

@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    list_display = ('client', 'name', 'id')
    list_filter = ('client', 'name')
    search_fields = ('name',)

@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'email', 'phone', 'job_type', 'places_of_work', 'client')
    list_filter = ('client',)
    search_fields = ('firstname', 'lastname', 'email', 'places_of_work')

    # def places_of_work_list(self, obj):
    #     return ", ".join([place.name for place in obj.places_of_work.all()])
    # places_of_work_list.short_description = 'Places of Work'
    # list_display += ('places_of_work_list',)

@admin.register(PlaceOfWorkCopy)
class PlaceOfWorkAdminCopy(admin.ModelAdmin):
    # list_display = ('name', 'client', 'address', 'id')
    list_display = ('name', 'address', 'id')
    # list_filter = ('client',)
    search_fields = ('name',)

@admin.register(InterestCopy)
class InterestAdminCopy(admin.ModelAdmin):
    # list_display = ('name', 'client', 'id')
    list_display = ('name', 'id')
    # list_filter = ('client',)
    search_fields = ('name',)

@admin.register(JobTypeCopy)
class JobTypeAdminCopy(admin.ModelAdmin):
    # list_display = ('client', 'name', 'id')
    list_display = ('name', 'id')
    # list_filter = ('client', 'name')
    search_fields = ('name',)

@admin.register(TargetCopy)
class TargetAdminCopy(admin.ModelAdmin):
    # list_display = ('id', 'firstname', 'lastname', 'email', 'phone', 'job_type', 'places_of_work', 'client', 'get_campaigns')
    list_display = ('id', 'firstname', 'lastname', 'email', 'phone', 'job_type', 'places_of_work', 'get_campaigns')
    # list_filter = ('client',)
    search_fields = ('firstname', 'lastname', 'email', 'places_of_work')
    
    @admin.display(description='Associated Campaigns')
    def get_campaigns(self, obj):
        if hasattr(obj, 'campaigns'):
            return ", ".join([str(campaign.id) for campaign in obj.campaigns.all()])

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'mode', 'created_at', 'start_date', 'end_date', 'updated_at', 'id')
    list_filter = ('type', 'mode')
    search_fields = ('name', 'description')

    def clients_list(self, obj):
        return ", ".join([client.name for client in obj.clients.all()])
    clients_list.short_description = 'Clients'
    
    list_display += ('clients_list',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('target', 'campaign', 'sent_at', 'delivery_status', 'id')
    list_filter = ('campaign', 'delivery_status')
    search_fields = ('target__firstname', 'target__lastname', 'campaign__name')

@admin.register(EventsLog)
class EventsLogAdmin(admin.ModelAdmin):
    list_display = ('type', 'date', 'message', 'id')
    search_fields = ('name', 'type')

@admin.register(FeedbacksCategory)
class FeedbacksCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)

@admin.register(FeedbacksType)
class FeedbacksTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'category', 'id')
    search_fields = ('name',)

@admin.register(FeedbacksLog)
class FeedbacksLogAdmin(admin.ModelAdmin):
    list_display = ('message', 'feedback_message', 'id')
    search_fields = ('name', 'message', 'feedback', 'feedback_type')
