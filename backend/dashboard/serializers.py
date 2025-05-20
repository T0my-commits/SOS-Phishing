from rest_framework import serializers

# Pour /get_campaign_info/
class CampaignInfoSerializer(serializers.Serializer):
    compromises = serializers.IntegerField(min_value=0)
    percentage_compromises = serializers.IntegerField(min_value=0)
    sent = serializers.IntegerField(min_value=0)
    percentage_to_be_sent = serializers.IntegerField()
    clicks = serializers.IntegerField(min_value=0)
    reports = serializers.IntegerField(min_value=0)
    download_attachments = serializers.IntegerField(min_value=0)
    open_attachments = serializers.IntegerField(min_value=0)
    creds_leak = serializers.IntegerField(min_value=0)
    nb_targets = serializers.IntegerField(min_value=0)
    feedbacks = serializers.IntegerField(min_value=0)
    percentage_feedbacks = serializers.IntegerField(min_value=0)
    percentage_current_signaling = serializers.IntegerField(min_value=0)
    percentage_expected_signaling = serializers.IntegerField()
    is_finished = serializers.BooleanField(default=True)
    is_archived = serializers.BooleanField(default=True)
    hours_elapsed = serializers.IntegerField()
    hours_remaining = serializers.IntegerField()
    mode = serializers.CharField()

# Pour /recent_activities/
class RecentActivitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    payload_sent_at = serializers.DateTimeField()
    event_date = serializers.DateTimeField()
    event_label = serializers.CharField()
    country = serializers.CharField()
    place_of_work = serializers.CharField()
    interests = serializers.ListField(child=serializers.CharField())
    job_type = serializers.CharField()

# Pour /activity_timeline/
class ActivityTimelineSerializer(serializers.Serializer):
    labels = serializers.ListField(child=serializers.CharField())
    data_compromises = serializers.ListField(child=serializers.IntegerField())
    data_clicks = serializers.ListField(child=serializers.IntegerField())
    data_signalisations = serializers.ListField(child=serializers.IntegerField())
    data_download_attachment = serializers.ListField(child=serializers.IntegerField())
    data_open_attachment = serializers.ListField(child=serializers.IntegerField())
    data_creds_leak = serializers.ListField(child=serializers.IntegerField())


# Pour /compromises_by_categories/ et /compromises_by_places_of_work/
class JobTypeDataSerializer(serializers.Serializer):
    job_type_name = serializers.CharField()
    job_type_data = serializers.ListField(child=serializers.IntegerField())

class CompromiseByGroupSerializer(serializers.Serializer):
    labels = serializers.ListField(child=serializers.CharField())
    data = JobTypeDataSerializer(many=True)


# Pour /feedbacks_radargraph/
class FeedbackRadarGraphSerializer(serializers.Serializer):
    labels = serializers.ListField(child=serializers.CharField())
    data = JobTypeDataSerializer(many=True)
