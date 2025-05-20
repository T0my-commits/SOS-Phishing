from django.contrib import messages
from django.utils import timezone

def add_campaign_status_messages(request, campaign):
    """Adds toast messages based on the campaign's status."""
    if campaign.end_date and timezone.now() > campaign.end_date:
        messages.success(request, 'This campaign is finished.')
    if campaign.is_archive:
        messages.info(request, 'This campaign is archived.')
