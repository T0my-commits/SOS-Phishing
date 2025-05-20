import random
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib import messages
from django_countries.fields import CountryField
import csv

from customization.forms import AddCsvForm, AddInterestForm, AddPlaceOfWorkForm, AddTargetForm
from shared_models.models import Client, Interest, JobType, PlaceOfWork, Target


# ░█▀█░█▀▄░█▀▄░░░▀█▀░█▀█░█▀▄░█▀▀░█▀▀░▀█▀░█▀▀
# ░█▀█░█░█░█░█░░░░█░░█▀█░█▀▄░█░█░█▀▀░░█░░▀▀█
# ░▀░▀░▀▀░░▀▀░░░░░▀░░▀░▀░▀░▀░▀▀▀░▀▀▀░░▀░░▀▀▀

class AddTargetsView(LoginRequiredMixin, View):
    template_name = 'customization/add_targets.html'
    login_url = 'login'
    
    def get(self, request):
        # breadcrumb
        breadcrumb_pages = [
            { 'label': 'Add targets', 'url': '' }
        ]

        return render(request, self.template_name, context={
            'breadcrumb_pages': breadcrumb_pages
        })

class AddTargetsManuallyView(LoginRequiredMixin, View):
    template_name = 'customization/add_targets_manually.html'
    login_url = 'login'
    
    def get(self, request):
        # get client
        user = request.user
        client_id = user.client.id if user.client else None
        client = get_object_or_404(Client, id=client_id)

        # get targets
        targets = client.targets.all()
        add_targets_form = AddTargetForm()
        add_targets_csv_form = AddCsvForm()

        # Prepare interests format
        targets_list = []
        for it in targets:
            interests = list(it.interests.values_list('name', flat=True))
            targets_list.append({
                'target': it,
                'firstname': it.firstname,
                'lastname': it.lastname,
                'email': it.email,
                'phone': it.phone,
                'address': it.address,
                'places_of_work': it.places_of_work,
                'interests': interests,
                'job_type': it.job_type
            })

        # breadcrumb
        breadcrumb_pages = [
            { 'label': 'Add targets', 'url': 'add_targets' },
            { 'label': 'Add manually' }
        ]

        return render(request, self.template_name, context={
            'breadcrumb_pages': breadcrumb_pages,
            'targets_list': targets_list,
            'add_targets_form': add_targets_form,
            'add_targets_csv_form': add_targets_csv_form
        })
    
    def post(self, request):
        form = AddTargetForm(request.POST)

        # check form validity
        if not form.is_valid():
            messages.error(request, 'Request is not valid, please retry.', extra_tags="")
            return redirect('add_targets_manually')

        # check client
        client = getattr(request.user, 'client', None)
        if not client:
            messages.error(request, 'User must be associated to a client.', extra_tags="")
            return redirect('add_targets_manually')

        # get data
        firstname = form.cleaned_data['firstname']
        lastname = form.cleaned_data['lastname']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']
        address = form.cleaned_data['address']
        country = form.cleaned_data['country']
        places_of_work = form.cleaned_data['places_of_work']
        job_type = form.cleaned_data['job_type']
        interests = form.cleaned_data['interests']

        # add target
        target = Target.objects.create(
            client=client,
            firstname=firstname,
            lastname=lastname,
            email=email,
            phone=phone,
            address=address,
            country=country,
            places_of_work=places_of_work,
            job_type=job_type,
        )
        target.interests.set(interests)
        target.save()

        messages.success(request, 'Target added successfully.', extra_tags="")
        return redirect('add_targets_manually')


# ░█▀█░█▀▄░█▀▄░░░▀█▀░█▀█░█▀▄░█▀▀░█▀▀░▀█▀░█▀▀░░░█▀▀░█▀▀░█░█
# ░█▀█░█░█░█░█░░░░█░░█▀█░█▀▄░█░█░█▀▀░░█░░▀▀█░░░█░░░▀▀█░▀▄▀
# ░▀░▀░▀▀░░▀▀░░░░░▀░░▀░▀░▀░▀░▀▀▀░▀▀▀░░▀░░▀▀▀░░░▀▀▀░▀▀▀░░▀░

class AddTargetsManuallyCsvView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        # check client
        client = getattr(request.user, 'client', None)
        if not client:
            messages.error(request, 'User must be associated to a client.', extra_tags="")
            return redirect('add_targets_manually')

        # get data
        targets = Target.objects.filter(client=client).values(
            'firstname', 'lastname', 'email', 'phone', 'address', 'country', 'places_of_work', 'interests', 'job_type'
        )

        # check data
        if not targets.exists():
            messages.info(request, 'No targets found for this client.', extra_tags="")
            return redirect('add_targets_manually')

        # generate CSV file
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="targets_{client}.csv"'

        writer = csv.DictWriter(response, fieldnames=[
            Target.csv_fields.FIRSTNAME,
            Target.csv_fields.LASTNAME,
            Target.csv_fields.EMAIL,
            Target.csv_fields.PHONE,
            Target.csv_fields.ADDRESS,
            Target.csv_fields.COUNTRY,
            Target.csv_fields.PLACES_OF_WORK,
            Target.csv_fields.INTERESTS,
            Target.csv_fields.JOB_TYPE
        ])
        writer.writeheader()

        for it in targets:
            writer.writerow({
                Target.csv_fields.FIRSTNAME: it['firstname'],
                Target.csv_fields.LASTNAME: it['lastname'],
                Target.csv_fields.EMAIL: it['email'],
                Target.csv_fields.PHONE: it['phone'],
                Target.csv_fields.ADDRESS: it['address'],
                Target.csv_fields.COUNTRY: it['country'],
                Target.csv_fields.PLACES_OF_WORK: it['places_of_work'],
                Target.csv_fields.INTERESTS: it['interests'],
                Target.csv_fields.JOB_TYPE: it['job_type'],
            })

        return response
    
    def post(self, request):
        form = AddCsvForm(request.POST, request.FILES)

        # check form validity
        if not form.is_valid():
            messages.error(request, 'Request is not valid, please retry.', extra_tags="")
            return redirect('add_targets_manually')
        
        # check client
        client = getattr(request.user, 'client', None)
        if not client:
            messages.error(request, 'User must be associated to a client.', extra_tags="")
            return redirect('add_targets_manually')

        # get data
        file = form.cleaned_data['file']
        keep_data = form.cleaned_data['keep_data']
        targets = Target.objects.filter(client=client).all()
        if not file:
            messages.error(request, 'An error occurs, please retry.', extra_tags="")
            return redirect('add_targets_manually')
        
        # clean database
        if not keep_data:
            targets.delete()

        # add targets
        try:
            # Lecture du fichier CSV
            decoded_file = file.read().decode('utf-8')
            csv_reader = csv.DictReader(decoded_file.splitlines())

            for row in csv_reader:
                # Si `keep_data` est activé et que la cible existe déjà, on passe
                # if keep_data and row[Target.csv_fields.NAME] in targets:
                #     continue

                # Recherche des objets liés pour les champs `places_of_work` et `job_type`
                try:
                    place_of_work = PlaceOfWork.objects.get(name=row[Target.csv_fields.PLACES_OF_WORK])
                except PlaceOfWork.DoesNotExist:
                    messages.error(request, f"Place of work '{row[Target.csv_fields.PLACES_OF_WORK]}' not found.")
                    continue

                try:
                    job_type = JobType.objects.get(name=row[Target.csv_fields.JOB_TYPE])
                except JobType.DoesNotExist:
                    messages.error(request, f"Job type '{row[Target.csv_fields.JOB_TYPE]}' not found.")
                    continue

                # Création de l'objet Target
                target = Target.objects.create(
                    client=client,
                    firstname=row[Target.csv_fields.FIRSTNAME],
                    lastname=row[Target.csv_fields.LASTNAME],
                    email=row[Target.csv_fields.EMAIL],
                    phone=row[Target.csv_fields.PHONE],
                    address=row[Target.csv_fields.ADDRESS],
                    country=row[Target.csv_fields.COUNTRY],
                    places_of_work=place_of_work,
                    job_type=job_type,
                )

                # Traitement des intérêts (séparés par des virgules)
                interests_names = [interest.strip() for interest in row[Target.csv_fields.INTERESTS].split(',') if interest.strip()]
                interests = Interest.objects.filter(name__in=interests_names)
                if len(interests) != len(interests_names):
                    missing = set(interests_names) - set(interests.values_list('name', flat=True))
                    messages.warning(request, f"Some interests were not found and skipped: {', '.join(missing)}.")

                # Ajout des intérêts au target
                target.interests.set(interests)

                # Sauvegarde de l'objet
                target.save()
        except Exception as e:
            messages.error(request, f'An error occurred while processing the file: {e}', extra_tags="")
            return redirect('add_targets_manually')

        return redirect('add_targets_manually')


# ░█▀█░█▀▄░█▀▄░░░▀█▀░█▀█░▀█▀░█▀▀░█▀▄░█▀▀░█▀▀░▀█▀░█▀▀
# ░█▀█░█░█░█░█░░░░█░░█░█░░█░░█▀▀░█▀▄░█▀▀░▀▀█░░█░░▀▀█
# ░▀░▀░▀▀░░▀▀░░░░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░▀▀▀░▀▀▀░░▀░░▀▀▀

class AddInterestsView(LoginRequiredMixin, View):
    template_name = 'customization/add_interests.html'
    login_url = 'login'
    
    def get(self, request):
        # get client
        user = request.user
        client_id = user.client.id if user.client else None

        # get interests
        interests_list = Interest.objects.filter(client=client_id).all()

        # create forms
        add_interest_form = AddInterestForm()
        add_interest_csv_form = AddCsvForm()

        # breadcrumb
        breadcrumb_pages = [
            { 'label': 'Add interests', 'url': '' }
        ]

        return render(request, self.template_name, context={
            'breadcrumb_pages': breadcrumb_pages,
            'interests_list': interests_list,
            'add_interest_form': add_interest_form,
            'add_interest_csv_form': add_interest_csv_form
        })
    
    def post(self, request):
        form = AddInterestForm(request.POST)

        # check form validity
        if not form.is_valid():
            messages.error(request, 'Request is not valid, please retry.', extra_tags="")
            return redirect('add_interests')

        # check client
        client = getattr(request.user, 'client', None)
        if not client:
            messages.error(request, 'User must be associated to a client.', extra_tags="")
            return redirect('add_interests')

        # check interest name
        name = form.cleaned_data['name']
        if not name:
            messages.error(request, 'The interest must have a name.', extra_tags="")
            return redirect('add_interests')

        # add interest
        Interest.objects.create(
            client=client,
            name=name
        )
        messages.success(request, 'Interest added successfully.', extra_tags="")
        return redirect('add_interests')


# ░█▀█░█▀▄░█▀▄░░░▀█▀░█▀█░▀█▀░█▀▀░█▀▄░█▀▀░█▀▀░▀█▀░█▀▀░░░█▀▀░█▀▀░█░█
# ░█▀█░█░█░█░█░░░░█░░█░█░░█░░█▀▀░█▀▄░█▀▀░▀▀█░░█░░▀▀█░░░█░░░▀▀█░▀▄▀
# ░▀░▀░▀▀░░▀▀░░░░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░▀▀▀░▀▀▀░░▀░░▀▀▀░░░▀▀▀░▀▀▀░░▀░

class AddInterestsCsvView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        # check client
        client = getattr(request.user, 'client', None)
        if not client:
            messages.error(request, 'User must be associated to a client.', extra_tags="")
            return redirect('add_interests')

        # get data
        interests = Interest.objects.filter(client=client).values('name')

        # check data
        if not interests.exists():
            messages.info(request, 'No interests found for this client.', extra_tags="")
            return redirect('add_interests')

        # generate CSV file
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="interests_{client}.csv"'

        writer = csv.DictWriter(response, fieldnames=[Interest.csv_fields.NAME])
        writer.writeheader()

        for it in interests:
            writer.writerow({
                Interest.csv_fields.NAME: it['name'],
            })

        return response
    
    def post(self, request):
        form = AddCsvForm(request.POST, request.FILES)

        # check form validity
        if not form.is_valid():
            messages.error(request, 'Request is not valid, please retry.', extra_tags="")
            return redirect('add_interests')
        
        # check client
        client = getattr(request.user, 'client', None)
        if not client:
            messages.error(request, 'User must be associated to a client.', extra_tags="")
            return redirect('add_interests')

        # get data
        file = form.cleaned_data['file']
        keep_data = form.cleaned_data['keep_data']
        interests = Interest.objects.filter(client=client).all()
        if not file:
            messages.error(request, 'An error occurs, please retry.', extra_tags="")
            return redirect('add_interests')
        
        # clean database
        if not keep_data:
            interests.delete()

        # add interests
        try:
            decoded_file = file.read().decode('utf-8')
            csv_reader = csv.DictReader(decoded_file.splitlines())
            for row in csv_reader:
                if keep_data and row[Interest.csv_fields.NAME] in interests:
                    continue
                Interest.objects.create(
                    client=client,
                    name=row[Interest.csv_fields.NAME],
                    color="#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
                )
            messages.success(request, 'Interests added successfully.', extra_tags="")
        except Exception as e:
            messages.error(request, f'An error occurred while processing the file: {e}', extra_tags="")
            return redirect('add_interests')

        return redirect('add_interests')


# ░█▀█░█▀▄░█▀▄░░░█▀█░█░░░█▀█░█▀▀░█▀▀░█▀▀░░░█▀█░█▀▀░░░█░█░█▀█░█▀▄░█░█
# ░█▀█░█░█░█░█░░░█▀▀░█░░░█▀█░█░░░█▀▀░▀▀█░░░█░█░█▀▀░░░█▄█░█░█░█▀▄░█▀▄
# ░▀░▀░▀▀░░▀▀░░░░▀░░░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░░░▀▀▀░▀░░░░░▀░▀░▀▀▀░▀░▀░▀░▀

class AddPlaceOfWorkView(LoginRequiredMixin, View):
    template_name = 'customization/add_place_of_work.html'
    login_url = 'login'
    
    def get(self, request):
        # get client
        user = request.user
        client_id = user.client.id if user.client else None

        # get interests
        places_of_work_list = PlaceOfWork.objects.filter(client=client_id).all()

        # create forms
        add_place_of_work_form = AddPlaceOfWorkForm()
        add_place_of_work_csv_form = AddCsvForm()

        # breadcrumb
        breadcrumb_pages = [
            { 'label': 'Add place of work', 'url': '' }
        ]

        return render(request, self.template_name, context={
            'breadcrumb_pages': breadcrumb_pages,
            'places_of_work_list': places_of_work_list,
            'add_place_of_work_form': add_place_of_work_form,
            'add_place_of_work_csv_form': add_place_of_work_csv_form
        })
    
    def post(self, request):
        form = AddPlaceOfWorkForm(request.POST)

        # check form validity
        if not form.is_valid():
            messages.error(request, 'Request is not valid, please retry.', extra_tags="")
            return redirect('add_place_of_work')

        # check client
        client = getattr(request.user, 'client', None)
        if not client:
            messages.error(request, 'User must be associated to a client.', extra_tags="")
            return redirect('add_place_of_work')

        # check place_of_work name
        name = form.cleaned_data['name']
        address = form.cleaned_data['address']
        country = form.cleaned_data['country']
        if not name or not country:
            messages.error(request, 'Some required values are missing, please try again.', extra_tags="")
            return redirect('add_place_of_work')

        # add place_of_work
        place_of_work = PlaceOfWork.objects.create(
            client=client,
            name=name,
            address=address,
            country=country
        )
        messages.success(request, 'Place of work added successfully.', extra_tags="")
        return redirect('add_place_of_work')


# ░█▀█░█▀▄░█▀▄░░░█▀█░█░░░█▀█░█▀▀░█▀▀░█▀▀░░░█▀█░█▀▀░░░█░█░█▀█░█▀▄░█░█░░░█▀▀░█▀▀░█░█
# ░█▀█░█░█░█░█░░░█▀▀░█░░░█▀█░█░░░█▀▀░▀▀█░░░█░█░█▀▀░░░█▄█░█░█░█▀▄░█▀▄░░░█░░░▀▀█░▀▄▀
# ░▀░▀░▀▀░░▀▀░░░░▀░░░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░░░▀▀▀░▀░░░░░▀░▀░▀▀▀░▀░▀░▀░▀░░░▀▀▀░▀▀▀░░▀░

class AddPlaceOfWorkCsvView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        # check client
        client = getattr(request.user, 'client', None)
        if not client:
            messages.error(request, 'User must be associated to a client.', extra_tags="")
            return redirect('add_place_of_work')

        # get data
        places_of_work = PlaceOfWork.objects.filter(client=client).values('name', 'address', 'country')

        # check data
        if not places_of_work.exists():
            messages.info(request, 'No places_of_work found for this client.', extra_tags="")
            return redirect('add_place_of_work')

        # generate CSV file
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="places_of_work_{client}.csv"'

        writer = csv.DictWriter(response, fieldnames=[
            PlaceOfWork.csv_fields.NAME,
            PlaceOfWork.csv_fields.ADDRESS,
            PlaceOfWork.csv_fields.COUNTRY
        ])
        writer.writeheader()

        for it in places_of_work:
            writer.writerow({
                PlaceOfWork.csv_fields.NAME: it['name'],
                PlaceOfWork.csv_fields.ADDRESS: it['address'],
                PlaceOfWork.csv_fields.COUNTRY: it['country'],
            })

        return response
    
    def post(self, request):
        form = AddCsvForm(request.POST, request.FILES)

        # check form validity
        if not form.is_valid():
            messages.error(request, 'Request is not valid, please retry.', extra_tags="")
            return redirect('add_place_of_work')
        
        # check client
        client = getattr(request.user, 'client', None)
        if not client:
            messages.error(request, 'User must be associated to a client.', extra_tags="")
            return redirect('add_place_of_work')

        # get data
        file = form.cleaned_data['file']
        keep_data = form.cleaned_data['keep_data']
        places_of_work = PlaceOfWork.objects.filter(client=client).all()
        if not file:
            messages.error(request, 'An error occurs, please retry.', extra_tags="")
            return redirect('add_place_of_work')
        
        # clean database
        if not keep_data:
            places_of_work.delete()

        # add places of work
        try:
            decoded_file = file.read().decode('utf-8')
            csv_reader = csv.DictReader(decoded_file.splitlines())
            for row in csv_reader:
                if keep_data and row[PlaceOfWork.csv_fields.NAME] in places_of_work:
                    continue
                PlaceOfWork.objects.create(
                    client=client,
                    name=row[PlaceOfWork.csv_fields.NAME],
                    address=row[PlaceOfWork.csv_fields.ADDRESS],
                    country=row[PlaceOfWork.csv_fields.COUNTRY]
                )
            messages.success(request, 'Place of work added successfully.', extra_tags="")
        except Exception as e:
            messages.error(request, f'An error occurred while processing the file: {e}', extra_tags="")
            return redirect('add_place_of_work')

        return redirect('add_place_of_work')