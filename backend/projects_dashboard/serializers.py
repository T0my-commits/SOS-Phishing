from rest_framework import serializers
from shared_models.models import Campaign
from django.utils import formats

class CampaignStatsSerializer(serializers.ModelSerializer):
    messages_sent = serializers.IntegerField()
    targets_compromises = serializers.IntegerField()
    
    class Meta:
        model = Campaign
        fields = ['name', 'created_at', 'start_date', 'end_date', 'mode', 'type', 'url_id', 'messages_sent', 'targets_compromises']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = formats.date_format(instance.created_at, 'SHORT_DATETIME_FORMAT').upper()
        representation['start_date'] = formats.date_format(instance.start_date, 'SHORT_DATETIME_FORMAT').upper()
        representation['end_date'] = formats.date_format(instance.end_date, 'SHORT_DATETIME_FORMAT').upper()
        representation['mode'] = instance.mode.capitalize()
        representation['type'] = instance.type.capitalize()
        return representation
