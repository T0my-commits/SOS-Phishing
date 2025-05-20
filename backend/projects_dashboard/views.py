from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from shared_models.models import Campaign
from .serializers import CampaignStatsSerializer
from django.http import HttpResponseForbidden
from django.utils import timezone, formats
from django.db.models import Count, Q

class ClientRequiredMixin:
    def has_permission(self, request):
        return bool(request.user.client)

class ProjectsDashboardAPI(APIView, ClientRequiredMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Vérifier que l'utilisateur a un client associé
        if not self.has_permission(request):
            return HttpResponseForbidden("Vous devez avoir un client associé pour accéder à cette vue.")
        
        # Récupérer le client associé à l'utilisateur
        user_client = request.user.client.id

        # Récupérer les campagnes en cours
        client_campaigns = Campaign.objects.filter(
            clients__id=user_client
        ).filter(
            is_archive__exact=False
        )

        campaigns_info = []
        for campaign in client_campaigns:
            # Trouver le nombre de cibles compromises
            messages_stats = Campaign.objects.get_campaign_info(campaign)

            campaigns_info.append({
                'name': campaign.name.capitalize(),
                'created_at': formats.date_format(campaign.created_at, 'SHORT_DATETIME_FORMAT').upper(),
                'start_date': formats.date_format(campaign.start_date, 'SHORT_DATETIME_FORMAT').upper(),
                'end_date': formats.date_format(campaign.end_date, 'SHORT_DATETIME_FORMAT').upper(),
                'mode': campaign.mode.capitalize(),
                'type': campaign.type.capitalize(),
                'url_id': campaign.url_id,
                'messages_sent': messages_stats['sent'],
                'targets_compromises': messages_stats['compromises']
            })

        # Récupérer les campagnes archivées
        client_archive = Campaign.objects.filter(
            clients__id=user_client
        ).filter(
            is_archive__exact=True
        )

        archives_info = []
        for campaign in client_archive:
            messages_stats = Campaign.objects.get_campaign_info(campaign)

            archives_info.append({
                'name': campaign.name.capitalize(),
                'created_at': formats.date_format(campaign.created_at, 'SHORT_DATETIME_FORMAT').upper(),
                'start_date': formats.date_format(campaign.start_date, 'SHORT_DATETIME_FORMAT').upper(),
                'end_date': formats.date_format(campaign.end_date, 'SHORT_DATETIME_FORMAT').upper(),
                'mode': campaign.mode.capitalize(),
                'type': campaign.type.capitalize(),
                'url_id': campaign.url_id,
                'messages_sent': messages_stats['sent'],
                'targets_compromises': messages_stats['compromises']
            })

        return Response({
            'client_campaigns': campaigns_info,
            'client_archives': archives_info
        })
