"""
URL configuration for sos_phishing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from authentication.views import CurrentUserView
from projects_dashboard.views import ProjectsDashboardAPI
from dashboard.views import CampaignViewSet

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# DRF Router
router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet, basename='campaign')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API – autres endpoints manuels
    path('api-auth/', include('rest_framework.urls')),
    path('api/projects-dashboard/', ProjectsDashboardAPI.as_view(), name='projects_dashboard_api'),

    # JWT auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/user/me/', CurrentUserView.as_view(), name='current_user'),

    # Campagnes API RESTful
    path('api/', include(router.urls)),

    # Swagger
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]




    # path('', TemplateView.as_view(template_name="base.html"), name='index'),

    # # authentication urls
    # path('login/', authentication.views.LoginPageView.as_view(), name='login'),
    # path('logout/', authentication.views.logout_page, name='logout'),

    # # dashboards urls
    # path('projects_dashboard/', projects_dashboard.views.ProjectsDashboardView.as_view(), name='projects_dashboard'),
    # path('dashboard/<str:campaign_url_id>/technical/', dashboard.views.DashboardTechnicalView.as_view(), name='dashboard_technical'),
    # path('dashboard/<str:campaign_url_id>/business/', dashboard.views.DashboardBusinessView.as_view(), name='dashboard_business'),
    # path('dashboard/<str:campaign_url_id>/options/', dashboard.views.DashboardOptionsView.as_view(), name='dashboard_options'),
    # path('dashboard/<str:campaign_url_id>/remediations/', dashboard.views.DashboardRemediationsView.as_view(), name='dashboard_remediations'),
    # path('dashboard/<str:campaign_url_id>/notes/', dashboard.views.CampaignNotes.as_view(), name='campaign_notes'),

    # # launch campaign urls
    # path('new-phishing-campaign/', launch_phishing_campaign.views.LaunchNewPhishingCampaignView.as_view(), name='launch_phishing_campaign'),

    # # customization urls
    # path('add-targets/', customization.views.AddTargetsView.as_view(), name='add_targets'),
    # path('add-targets/add-manually/', customization.views.AddTargetsManuallyView.as_view(), name="add_targets_manually"),
    # path('add-targets/add-manually/csv/', customization.views.AddTargetsManuallyCsvView.as_view(), name="add_targets_csv"),

    # path('add-interests/', customization.views.AddInterestsView.as_view(), name='add_interests'),
    # path('add-interests/csv/', customization.views.AddInterestsCsvView.as_view(), name='add_interests_csv'),

    # path('add-place-of-work/', customization.views.AddPlaceOfWorkView.as_view(), name='add_place_of_work'),
    # path('add-place-of-work/csv/', customization.views.AddPlaceOfWorkCsvView.as_view(), name='add_place_of_work_csv'),
