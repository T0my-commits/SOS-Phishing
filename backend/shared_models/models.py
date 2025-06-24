import random
from django.db import models
from django_countries.fields import CountryField
from django_countries.fields import Country
from django.db.models import Count, Q, Value, Sum
from django.db.models import F, Case, When, ExpressionWrapper, FloatField, Func
from django.db.models.functions import Cast
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import m2m_changed
from django.utils import timezone
from django.dispatch import receiver
from datetime import timedelta
from rest_framework.request import Request
from collections import defaultdict
from types import SimpleNamespace
from enum import Enum


class EventsType(Enum):
    CLICK = 'click'
    DOWNLOAD_ATTACHMENT = 'download_attachements'
    OPENED_ATTACHMENT = 'open_attachements'
    CREDENTIALS_LEAK = 'credentials_leak'
    REPORT = 'report'



# ░█▀▀░█░░░▀█▀░█▀▀░█▀█░▀█▀
# ░█░░░█░░░░█░░█▀▀░█░█░░█░
# ░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░▀░

class Client(models.Model):
    """Represents a client using the marketing email service."""
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True) # blank=False
    address = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



# ░█▀▀░█▀█░█▀▀░█▀█░▀█▀░▀█▀░▀█▀░█░█░█▀▀░░░█▀▄░▀█▀░█▀█░█▀▀░█▀▀░█▀▀
# ░█░░░█░█░█░█░█░█░░█░░░█░░░█░░▀▄▀░█▀▀░░░█▀▄░░█░░█▀█░▀▀█░█▀▀░▀▀█
# ░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░░▀░░▀▀▀░░▀░░▀▀▀░░░▀▀░░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀

class CognitiveBiases(models.Model):
    """ Enumeration of cognitive biases in use. """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)



# ░█▀▀░█▀█░█▄█░█▀█░█▀█░▀█▀░█▀▀░█▀█░░░█▀▄░█░█░█▀█░█░░░▀█▀░█▀▀░█▀█░▀█▀░▀█▀░█▀█░█▀█░░
# ░█░░░█▀█░█░█░█▀▀░█▀█░░█░░█░█░█░█░░░█░█░█░█░█▀▀░█░░░░█░░█░░░█▀█░░█░░░█░░█░█░█░█░░
# ░▀▀▀░▀░▀░▀░▀░▀░░░▀░▀░▀▀▀░▀▀▀░▀░▀░░░▀▀░░▀▀▀░▀░░░▀▀▀░▀▀▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀▀▀░▀░▀░░
# ░█▀▀░█▀▀░█▀▄░█░█░▀█▀░█▀▀░█▀▀                                                    
# ░▀▀█░█▀▀░█▀▄░▀▄▀░░█░░█░░░█▀▀                                                    
# ░▀▀▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀▀▀░▀▀▀

class CampaignDuplicationService:
    def __init__(self, campaign, request:Request):
        self.campaign = campaign
        self.request = request

    def duplicate(self, targets_list:list=None, **kwargs) -> int:
        """  We duplicate all DB instances that is binded to the element in *Copy classes. """
        # creating a connector structure that will bind two elements
        class Connector:
            def __init__(self, orig=None, copy=None):
                self.orig = orig
                self.copy = copy

        # get client id from user
        client = getattr(self.request.user, 'client', None)
        if not client:
            raise ValueError("The current user is not associated with a client.")

        # duplicate places of work
        conn_places = []
        places = PlaceOfWork.objects.filter(client=client).all()
        for it in places:
            copy = it.duplicate(campaign_id=self.campaign.id)
            conn_places.append(Connector(orig=it, copy=copy))

        # duplicate interests
        conn_interests = []
        interests = Interest.objects.filter(client=client).all()
        for it in interests:
            copy = it.duplicate(campaign_id=self.campaign.id)
            conn_interests.append(Connector(orig=it, copy=copy))

        # duplicate job types
        conn_job_types = []
        job_types = JobType.objects.filter(client=client).all()
        for it in job_types:
            copy = it.duplicate(campaign_id=self.campaign.id)
            conn_job_types.append(Connector(orig=it, copy=copy))

        # duplicate targets
        for it in targets_list:
            copy = it.duplicate(
                places_of_work=[el.copy for el in conn_places if el.orig == it.places_of_work][0],
                job_types=[el.copy for el in conn_job_types if el.orig == it.job_type][0],
                interests=[el.copy for el in conn_interests if el.orig in it.interests.all()],
                campaign_id=self.campaign.id
            )
        
        return 0



# ░█▀▀░█▀█░█▄█░█▀█░█▀█░▀█▀░█▀▀░█▀█░░░█▄█░█▀█░█▀█░█▀█░█▀▀░█▀▀░█▀▄
# ░█░░░█▀█░█░█░█▀▀░█▀█░░█░░█░█░█░█░░░█░█░█▀█░█░█░█▀█░█░█░█▀▀░█▀▄
# ░▀▀▀░▀░▀░▀░▀░▀░░░▀░▀░▀▀▀░▀▀▀░▀░▀░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀

class CampaignManager(models.Manager):

    def get_campaign_info(self, campaign):
        """ Returns information about the campaign messages. """
        stats = Campaign.objects.filter(id=campaign.id).annotate(
            compromises=Count(
                'messages', 
                filter=Q(messages__events__type=campaign.compromise_type),
                distinct=True
            ),
            sent=Count('messages', distinct=True),
            clicks=Count('messages', filter=Q(messages__events__type=EventsType.CLICK.value)),
            reports=Count('messages', filter=Q(messages__events__type=EventsType.REPORT.value)),
            download_attachments=Count('messages', filter=Q(messages__events__type=EventsType.DOWNLOAD_ATTACHMENT.value)),
            open_attachments=Count('messages', filter=Q(messages__events__type=EventsType.OPENED_ATTACHMENT.value)),
            creds_leak=Count('messages', filter=Q(messages__events__type=EventsType.CREDENTIALS_LEAK.value)),
            feedbacks=Count('messages__feedback', filter=Q(messages__feedback__message__gt=0), distinct=True),
            nb_targets=Count('targets')
        ).values(
            'compromises', 'sent', 'clicks', 'reports', 'download_attachments', 'open_attachments', 'creds_leak', 
            'feedbacks', 'expected_signaling', 'nb_targets'
        ).first()

        # Calcul des pourcentages en Python pour éviter les erreurs de types
        if not stats:
            return None
        
        # Pourcentage de feedbacks
        percentage_feedbacks = 0
        if stats['compromises'] > 0:
            percentage_feedbacks = round(stats['feedbacks'] * 100.0 / stats['compromises'], 2)
        
        # Signaling actuel
        current_signaling = 0
        if stats['sent'] > 0:
            current_signaling = round(stats['reports'] * 100.0 / stats['sent'], 2)
        
        # Pourcentage de compromises
        percentage_compromises = 0
        if stats['sent'] > 0:
            percentage_compromises = round(stats['compromises'] * 100.0 / stats['sent'], 2)

        # Campaign information
        stats['mode'] = campaign.type.capitalize()
        stats['percentage_expected_signaling'] = int(stats['expected_signaling'])
        stats['hours_elapsed'] = int(campaign.hours_elapsed())
        stats['hours_remaining'] = int(campaign.hours_remaining()[0])
        stats['percentage_to_be_sent'] = 100 if int(stats['sent'] == 0) else int(int(stats['nb_targets']) * 100 / int(stats['sent']))
        stats['is_finished'] = True if campaign.end_date and timezone.now() > campaign.end_date else False
        stats['is_archived'] = campaign.is_archive
        stats['percentage_feedbacks'] = percentage_feedbacks
        stats['percentage_current_signaling'] = current_signaling
        stats['percentage_compromises'] = percentage_compromises

        return stats
    
    def get_recent_activities(self, campaign):
        # Get 
        self.query_messages_log = EventsLog.objects.filter(
            message__campaign_id=campaign.id
        ).select_related(
            'message__target'
        ).order_by('-date').all()

        # Create event list
        events = []
        for it in self.query_messages_log:
            events.append({
                "id": it.id,
                "payload_sent_at": it.message.sent_at,
                "event_date": it.date,
                "event_label": it.type.capitalize().replace('_', ' '),
                "country": it.message.target.places_of_work.country_name,
                "place_of_work": it.message.target.places_of_work.name,
                "interests": list(it.message.target.interests.values_list('name', flat=True)),
                "job_type": it.message.target.job_type.name
            })
        self.events = events
        return self.events

    def get_activity_timeline(self, campaign):
        # Détermine la durée de la timeline en fonction de `current_duration`
        now = timezone.now()
        current_duration = min(now, campaign.end_date) - campaign.start_date
        if current_duration.total_seconds() < 3600:  # less than one hour
            interval = timedelta(minutes=1)
            format_label = "%H:%M"
        elif current_duration.total_seconds() < 86400:  # less than one day
            interval = timedelta(hours=1)
            format_label = "%Y-%m-%d %H:%M"
        elif current_duration.total_seconds() < 2592000:  # less than a month
            interval = timedelta(days=1)
            format_label = "%Y-%m-%d"
        elif current_duration.total_seconds() < 31536000:  # less than a year
            interval = timedelta(weeks=1)
            format_label = "%Y-%m-%d"
        else:  # other cases
            interval = timedelta(weeks=4)
            format_label = "%Y-%m"

        # Initialisation des listes pour le dictionnaire `activity_timeline`
        activity_timeline = {
            'labels': [],
            'data_compromises': [],
            'data_clicks': [],
            'data_signalisations': [],
            'data_download_attachment': [],
            'data_open_attachment': [],
            'data_creds_leak': []
        }

        # Initialiser les variables pour l'itération
        current_time = campaign.start_date
        while current_time <= min(now, campaign.end_date):
            # Formatage des labels de temps
            label = current_time.strftime(format_label)
            activity_timeline['labels'].append(label)

            # Compter les événements pour cet intervalle
            next_time = current_time + interval
            events_timeline = EventsLog.objects.filter(
                message__campaign=campaign.id,
                date__gte=current_time,
                date__lt=next_time
            )

            # Remplissage des données par type d’événement
            activity_timeline['data_compromises'].append(events_timeline.filter(type=campaign.compromise_type).count())
            activity_timeline['data_clicks'].append(events_timeline.filter(type=EventsType.CLICK.value).count())
            activity_timeline['data_signalisations'].append(events_timeline.filter(type=EventsType.REPORT.value).count())
            activity_timeline['data_download_attachment'].append(events_timeline.filter(type=EventsType.DOWNLOAD_ATTACHMENT.value).count())
            activity_timeline['data_open_attachment'].append(events_timeline.filter(type=EventsType.OPENED_ATTACHMENT.value).count())
            activity_timeline['data_creds_leak'].append(events_timeline.filter(type=EventsType.CREDENTIALS_LEAK.value).count())

            # Passer à l'intervalle de temps suivant
            current_time = next_time
        return activity_timeline
    
    def get_messages_stats_by_job_type(self, campaign):
        return (
            EventsLog.objects
            .filter(message__campaign=campaign)
            .values('message__target__job_type__name')  # Group by job type
            .annotate(
                clicks=Count('id', filter=Q(type='click')),
                reports=Count('id', filter=Q(type='report')),
                download_attachments=Count('id', filter=Q(type='download_attachment')),
                open_attachments=Count('id', filter=Q(type='opened_attachment')),
                creds_leak=Count('id', filter=Q(type='credentials_leak')),
            )
        )
    
    def get_compromises_by_categories(self, campaign):
        query_job_type_counts = Campaign.objects.get_messages_stats_by_job_type(campaign)
        compromises_categories = {
            'labels': [
                'Clicks',
                'Reports',
                'Download attachments',
                'Open attachments',
                'Credentials leak'
            ],
            'data': []
        }
        for it in query_job_type_counts:
            compromises_categories['data'].append({
                'job_type_name': it['message__target__job_type__name'],
                'job_type_data': [
                    it['clicks'],
                    it['reports'],
                    it['download_attachments'],
                    it['open_attachments'],
                    it['creds_leak'],
                ]
            })
        return compromises_categories
    
    def get_compromises_by_places_of_work(self, campaign):
        query_job_type_counts = campaign.get_messages_stats_by_places_of_work()
        compromises_places_of_work = {
            'labels': [
                'Clicks',
                'Reports',
                'Download attachments',
                'Open attachments',
                'Credentials leak'
            ],
            'data': []
        }
        for it in query_job_type_counts:
            compromises_places_of_work['data'].append({
                'job_type_name': it['message__target__places_of_work__name'],
                'job_type_data': [
                    it['clicks'],
                    it['reports'],
                    it['download_attachments'],
                    it['open_attachments'],
                    it['creds_leak'],
                ]
            })
        return compromises_places_of_work



# ░█▀▀░█▀█░█▄█░█▀█░█▀█░▀█▀░█▀▀░█▀█
# ░█░░░█▀█░█░█░█▀▀░█▀█░░█░░█░█░█░█
# ░▀▀▀░▀░▀░▀░▀░▀░░░▀░▀░▀▀▀░▀▀▀░▀░▀

class Campaign(models.Model):
    """A phishing campain."""

    CAMPAIGN_TYPES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
    ]

    MODES = [
        ('auto', 'Automatic'),
        ('manual', 'Manual'),
    ]

    COMPROMISE_TYPES = [
        (EventsType.CLICK.value, 'User has clicked on the malicious link'),
        (EventsType.DOWNLOAD_ATTACHMENT.value, 'User has downloaded the attachments'),
        (EventsType.OPENED_ATTACHMENT.value, 'User has opened the attachments'),
        (EventsType.CREDENTIALS_LEAK.value, 'User has leaked some credentials'),
    ]

    clients = models.ManyToManyField(
        Client, 
        blank=False, 
        related_name='campaigns'
    )
    name = models.CharField(
        max_length=255
    )
    url_id = models.CharField(
        max_length=21, 
        null=False, 
        blank=False, 
        unique=True
    )
    description = models.TextField()

    type = models.CharField(
        max_length=10, 
        choices=CAMPAIGN_TYPES, 
        default='email'
    )
    mode = models.CharField(
        max_length=10, 
        choices=MODES, 
        default='auto'
    )
    expected_signaling = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(100)
        ], 
        default=20, 
        help_text="Expected signaling for this campain. Enter a percentage value between 0 and 100"
    )
    compromise_type = models.CharField(
        max_length=25, 
        blank=False, 
        null=False, 
        choices=COMPROMISE_TYPES, 
        default='click', 
        help_text="When is a target considered compromised?"
    )
    notes = models.TextField(
        blank=True, 
        null=True
    )
    arbitrary_failures = models.PositiveIntegerField(
        default=0
    )
    start_date = models.DateTimeField(
        blank=False, 
        null=False, 
        default=timezone.now, 
        help_text="Start date of the campaign"
    )
    end_date = models.DateTimeField(
        blank=False, 
        null=False, 
        default=None, 
        help_text="End date of the campaign"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    is_archive = models.BooleanField(
        default=False
    )
    objects = CampaignManager()

    def __str__(self):
        return self.name
    
    def save(self, targets_list:list=[], **kwargs):
        """ Save method override.
            We duplicate all DB instances that is binded to the element in *Copy classes.
        """
        # check for request variable
        self.request = kwargs.pop('request', None)
        if not self.request:
            return super().save(**kwargs)

        # duplicate all structures
        duplication_service = CampaignDuplicationService(self, kwargs.get('request'))
        duplication_service.duplicate(targets_list)

        # save object
        return super().save(**kwargs)

    def get_feedbacks_stats(self):
        """ Returns information about the campaign feedback sorted by categories,
            including counts by job types.
        """
        feedback_categories = (
            FeedbacksCategory.objects.annotate(
                count=Count('feedbacks_types__feedbacks_logs')
            )
            .values('id', 'name', 'count', 'view_color', 'view_icon')
        )
        feedback_types = (
            FeedbacksType.objects.annotate(
                count=Count('feedbacks_logs')
            )
            .values('id', 'name', 'count', 'category_id')
        )

        # Comptage des feedbacks par job_type et feedback_type
        feedbacks_by_job_type = (
            FeedbacksLog.objects.filter(message__campaign_id=self.id)
            .values(job_type_name=F('message__target__job_type__name'), feedback_type_id=F('feedback_type'))
            .annotate(count=Count('id'))
        )

        # Organisation des données : feedback_type_id -> job_type -> count
        feedback_type_to_job_type_counts = defaultdict(lambda: defaultdict(int))
        for entry in feedbacks_by_job_type:
            feedback_type_to_job_type_counts[entry['feedback_type_id']][entry['job_type_name']] = entry['count']

        # Organisation des types de feedbacks par catégorie
        category_to_types = defaultdict(list)
        for feedback_type in feedback_types:
            feedback_type_id = feedback_type['id']
            feedback_type['type'] = 'type'
            feedback_type['count_by_job_types'] = feedback_type_to_job_type_counts[feedback_type_id]
            category_to_types[feedback_type['category_id']].append(feedback_type)

        # Construction de la liste triée
        sorted_feedbacks = []
        for category in feedback_categories:
            category_id = category['id']
            category['type'] = 'category'
            category['count_by_job_types'] = defaultdict(int)

            # Agréger les données `count_by_job_types` pour chaque catégorie
            for feedback_type in category_to_types[category_id]:
                for job_type, count in feedback_type['count_by_job_types'].items():
                    category['count_by_job_types'][job_type] += count

            sorted_feedbacks.append(category)
            sorted_feedbacks.extend(category_to_types[category_id])

        return sorted_feedbacks

    def hours_remaining(self):
        """Returns the number of hours remaining until the end of the campaign."""
        now = timezone.now()
        if self.end_date and now < self.end_date:
            delta = self.end_date - now
            hours_remaining = delta.total_seconds() / 3600
            return (int(round(hours_remaining, 2)), round(hours_remaining, 2))
        else:
            return (0,)
        
    def hours_elapsed(self):
        """Returns the number of hours elapsed since the start of the campaign."""
        now = timezone.now()
        if self.start_date and now > self.start_date:
            if self.end_date and now < self.end_date:
                delta = now - self.start_date
                hours_elapsed = delta.total_seconds() / 3600
                return round(hours_elapsed, 2)
            else:
                delta = self.end_date - self.start_date
                hours_elapsed = delta.total_seconds() / 3600
                return round(hours_elapsed, 2)
        else:
            return 0


# ░█▀█░█░░░█▀█░█▀▀░█▀▀░░░█▀█░█▀▀░░░█░█░█▀█░█▀▄░█░█
# ░█▀▀░█░░░█▀█░█░░░█▀▀░░░█░█░█▀▀░░░█▄█░█░█░█▀▄░█▀▄
# ░▀░░░▀▀▀░▀░▀░▀▀▀░▀▀▀░░░▀▀▀░▀░░░░░▀░▀░▀▀▀░▀░▀░▀░▀

class PlaceOfWork(models.Model):
    """Represents a place of work for targets in various contexts."""

    csv_fields = SimpleNamespace(
        NAME='place_of_work_name',
        ADDRESS='place_of_work_address',
        COUNTRY='place_of_work_country'
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='places_of_work')
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    country = CountryField(blank=False)

    def __str__(self):
        return self.name

    @property
    def country_name(self):
        """Returns the full name of the country."""
        if self.country:
            country_code = self.country.code
            # flag = ''.join(chr(127397 + ord(c)) for c in country_code)
            flag = Country(code=country_code).unicode_flag
            return f"{flag} {Country(code=country_code).name}"
        return None
    
    def duplicate(self, campaign_id:int):
        return PlaceOfWorkCopy.objects.create(
            name=self.name,
            address=self.address,
            country=self.country,
            campaign=campaign_id
        )

class PlaceOfWorkCopy(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    country = CountryField(blank=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, blank=True, null=True, related_name='places_of_work')

    def __str__(self):
        return self.name
    
    @property
    def country_name(self):
        """Returns the full name of the country."""
        if self.country:
            country_code = self.country.code
            flag = Country(code=country_code).unicode_flag
            return f"{flag} {Country(code=country_code).name}"
        return None


# ░▀█▀░█▀█░▀█▀░█▀▀░█▀▄░█▀▀░█▀▀░▀█▀
# ░░█░░█░█░░█░░█▀▀░█▀▄░█▀▀░▀▀█░░█░
# ░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░▀▀▀░▀▀▀░░▀░

class Interest(models.Model):
    """Represents an interest that can be assigned to targets."""

    csv_fields = SimpleNamespace(
        NAME='interest_name',
        COLOR='interest_color'
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='interests')
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=10, default="#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)]))

    def __str__(self):
        return self.name
    
    def duplicate(self, campaign_id:int):
        return InterestCopy.objects.get_or_create(
            name=self.name,
            color=self.color,
            campaign=campaign_id
        )[0]

class InterestCopy(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=10)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, blank=True, null=True, related_name='interests')

    def __str__(self):
        return self.name


# ░▀▀█░█▀█░█▀▄░░░▀█▀░█░█░█▀█░█▀▀
# ░░░█░█░█░█▀▄░░░░█░░░█░░█▀▀░█▀▀
# ░▀▀░░▀▀▀░▀▀░░░░░▀░░░▀░░▀░░░▀▀▀

class JobType(models.Model):
    """ Represent a job category (ex.: executive, factory worker, IT technician, etc.) """

    csv_fields = SimpleNamespace(
        NAME='job_type_name'
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='job_types')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    def duplicate(self, campaign_id:int):
        return JobTypeCopy.objects.create(
            name=self.name,
            campaign=campaign_id
        )

class JobTypeCopy(models.Model):
    name = models.CharField(max_length=255)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, blank=True, null=True, related_name='job_types')

    def __str__(self):
        return self.name


# ░▀█▀░█▀█░█▀▄░█▀▀░█▀▀░▀█▀
# ░░█░░█▀█░█▀▄░█░█░█▀▀░░█░
# ░░▀░░▀░▀░▀░▀░▀▀▀░▀▀▀░░▀░

class Target(models.Model):
    """Represents a target audience or user profile."""

    csv_fields = SimpleNamespace(
        FIRSTNAME='target_firstname',
        LASTNAME='target_lastname',
        EMAIL='target_email',
        PHONE='target_phone',
        ADDRESS='target_address',
        COUNTRY='target_country',
        PLACES_OF_WORK='target_places_of_work',
        INTERESTS='target_interests',
        JOB_TYPE='target_job_type',
    )

    is_snapshot = models.BooleanField(
        default=False
    )

    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='targets'
    )

    firstname = models.CharField(
        max_length=255
    )

    lastname = models.CharField(
        max_length=255
    )

    email = models.EmailField(
        blank=True, 
        null=True
    )
    
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True
    )
    
    address = models.TextField(
        blank=True, 
        null=True
    )
    
    country = CountryField(
        blank=True
    )
    
    places_of_work = models.ForeignKey(
        PlaceOfWork, 
        on_delete=models.DO_NOTHING, 
        blank=True, 
        null=True, 
        related_name='targets'
    )
    
    interests = models.ManyToManyField(
        Interest, 
        blank=True, 
        related_name='targets'
    )
    
    job_type = models.ForeignKey(
        JobType, 
        on_delete=models.DO_NOTHING, 
        blank=True, 
        null=True, 
        related_name='targets'
    )

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    def duplicate(self, places_of_work:list=None, job_types:list=None, interests:list=None, campaign_id:int=None):
        ret = TargetCopy.objects.create(
            campaign=campaign_id,
            firstname=self.firstname,
            lastname=self.lastname,
            email=self.email,
            phone=self.phone,
            address=self.address,
            places_of_work=places_of_work if places_of_work else self.places_of_work.duplicate(),
            job_type=job_types if job_types else self.job_type.duplicate()
        )
        if interests:
            ret.interests.set(interests)
        else:
            ret.interests.set([it.duplicate() for it in self.interests.all()])
        ret.save()
        return ret

class TargetCopy(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, blank=True, null=True, related_name='targets')
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(blank=False, null=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    places_of_work = models.ForeignKey(PlaceOfWorkCopy, on_delete=models.CASCADE, blank=False, null=False, related_name='targets')
    interests = models.ManyToManyField(InterestCopy, blank=True, related_name='targets')
    job_type = models.ForeignKey(JobTypeCopy, on_delete=models.CASCADE, blank=False, null=False, related_name='targets')

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


# ░█▄█░█▀▀░█▀▀░█▀▀░█▀█░█▀▀░█▀▀
# ░█░█░█▀▀░▀▀█░▀▀█░█▀█░█░█░█▀▀
# ░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀

class Message(models.Model):
    """Tracks individual messages sent in a campaign."""

    DELIVERY_STATUS = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
    ]

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='messages')
    target = models.ForeignKey(TargetCopy, on_delete=models.CASCADE, related_name='messages')
    sent_at = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=40, choices=DELIVERY_STATUS, default="pending")

    def __str__(self):
        return f"Message to {self.target.firstname} {self.target.lastname.upper()} for {self.campaign.name}"


# ░█▀▀░█░█░█▀▀░█▀█░▀█▀░█▀▀░░░█░░░█▀█░█▀▀
# ░█▀▀░▀▄▀░█▀▀░█░█░░█░░▀▀█░░░█░░░█░█░█░█
# ░▀▀▀░░▀░░▀▀▀░▀░▀░░▀░░▀▀▀░░░▀▀▀░▀▀▀░▀▀▀

class EventsLog(models.Model):
    """ Tracks all events that happens during a campaign. """

    EVENT_TYPES = [
        (EventsType.CLICK.value, 'Click'),
        (EventsType.DOWNLOAD_ATTACHMENT.value, 'Download attachment'),
        (EventsType.OPENED_ATTACHMENT.value, 'Open attachment'),
        (EventsType.CREDENTIALS_LEAK.value, 'Credentials leak'),
        (EventsType.REPORT.value, 'Report')
    ]

    type = models.CharField(max_length=30, choices=EVENT_TYPES, help_text="Type of event triggered")
    date = models.DateTimeField(null=True, blank=True, help_text="Timestamp of when the event have been triggered")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='events', blank=False, null=False)


# ░█▀▀░█▀▀░█▀▀░█▀▄░█▀▄░█▀█░█▀▀░█░█░█▀▀░░░█▀▀░█▀█░▀█▀░█▀▀░█▀▀░█▀█░█▀▄░▀█▀░█▀▀░█▀▀
# ░█▀▀░█▀▀░█▀▀░█░█░█▀▄░█▀█░█░░░█▀▄░▀▀█░░░█░░░█▀█░░█░░█▀▀░█░█░█░█░█▀▄░░█░░█▀▀░▀▀█
# ░▀░░░▀▀▀░▀▀▀░▀▀░░▀▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░░░▀▀▀░▀░▀░░▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀

class FeedbacksCategory(models.Model):
    """ Category of user feedback after compromission. """
    name = models.CharField(max_length=255, blank=False, null=False)
    view_class = models.CharField(max_length=255, blank=True, null=True)
    view_color = models.CharField(max_length=255, blank=True, null=True)
    view_icon = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


# ░█▀▀░█▀▀░█▀▀░█▀▄░█▀▄░█▀█░█▀▀░█░█░█▀▀░░░▀█▀░█░█░█▀█░█▀▀░█▀▀
# ░█▀▀░█▀▀░█▀▀░█░█░█▀▄░█▀█░█░░░█▀▄░▀▀█░░░░█░░░█░░█▀▀░█▀▀░▀▀█
# ░▀░░░▀▀▀░▀▀▀░▀▀░░▀▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░░░░▀░░░▀░░▀░░░▀▀▀░▀▀▀

class FeedbacksType(models.Model):
    """ Type of feedbacks. """
    name = models.CharField(max_length=255, blank=False, null=False)
    label = models.CharField(max_length=255, blank=False, null=False)
    category = models.ForeignKey(FeedbacksCategory, on_delete=models.DO_NOTHING, related_name="feedbacks_types", blank=True, null=True)

    def __str__(self):
        return self.name


# ░█▀▀░█▀▀░█▀▀░█▀▄░█▀▄░█▀█░█▀▀░█░█░█▀▀░░░█░░░█▀█░█▀▀
# ░█▀▀░█▀▀░█▀▀░█░█░█▀▄░█▀█░█░░░█▀▄░▀▀█░░░█░░░█░█░█░█
# ░▀░░░▀▀▀░▀▀▀░▀▀░░▀▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░░░▀▀▀░▀▀▀░▀▀▀

class FeedbacksLog(models.Model):
    """ Track all user feedback that have been compromises. """
    message = models.OneToOneField(Message, on_delete=models.DO_NOTHING, related_name="feedback")
    feedback_message = models.TextField(blank=True, null=True)
    feedback_type = models.ManyToManyField(FeedbacksType, blank=True, related_name="feedbacks_logs")

    def __str__(self):
        return f"Feedback of {self.message.target.firstname} {self.message.target.lastname.upper()} to message {self.message.id}"
