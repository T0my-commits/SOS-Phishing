from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import (
    CampaignInfoSerializer,
    RecentActivitySerializer,
    ActivityTimelineSerializer,
    CompromiseByGroupSerializer
)
from shared_models.models import Campaign
from django.shortcuts import get_object_or_404


class CampaignViewSet(ViewSet):

    def get_campaign(self, pk):
        return get_object_or_404(Campaign, url_id=pk)

    @extend_schema(
        responses=CampaignInfoSerializer,
        description="Statistiques d'ensemble sur la campagne",
        summary="Statistiques de campagne"
    )
    @action(detail=True, methods=['get'])
    def get_campaign_info(self, request, pk=None):
        campaign = self.get_campaign(pk)
        data = Campaign.objects.get_campaign_info(campaign)
        serializer = CampaignInfoSerializer(data)
        return Response(serializer.data)

    @extend_schema(
        responses=RecentActivitySerializer(many=True),
        description="Liste des activités récentes pour une campagne donnée.",
        summary="Activité récente"
    )
    @action(detail=True, methods=['get'])
    def recent_activities(self, request, pk=None):
        campaign = self.get_campaign(pk)
        data = Campaign.objects.get_recent_activities(campaign)
        serializer = RecentActivitySerializer(data, many=True)
        return Response(serializer.data)

    @extend_schema(
        responses=ActivityTimelineSerializer,
        description="Timeline des événements d'une campagne, regroupés par intervalle temporel adapté.",
        summary="Timeline des événements"
    )
    @action(detail=True, methods=['get'])
    def activity_timeline(self, request, pk=None):
        campaign = self.get_campaign(pk)
        data = Campaign.objects.get_activity_timeline(campaign)
        serializer = ActivityTimelineSerializer(data)
        return Response(serializer.data)

    @extend_schema(
        responses=CompromiseByGroupSerializer,
        description="Compromissions réparties par type de job.",
        summary="Compromissions par métier"
    )
    @action(detail=True, methods=['get'])
    def compromises_by_categories(self, request, pk=None):
        campaign = self.get_campaign(pk)
        data = Campaign.objects.get_compromises_by_categories(campaign)
        serializer = CompromiseByGroupSerializer(data)
        return Response(serializer.data)

    @extend_schema(
        responses=CompromiseByGroupSerializer,
        description="Compromissions réparties par lieu de travail.",
        summary="Compromissions par lieu"
    )
    @action(detail=True, methods=['get'])
    def compromises_by_places_of_work(self, request, pk=None):
        campaign = self.get_campaign(pk)
        data = Campaign.objects.get_compromises_by_places_of_work(campaign)
        serializer = CompromiseByGroupSerializer(data)
        return Response(serializer.data)
