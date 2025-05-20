from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib import messages

from shared_models.models import Campaign
from .forms import LaunchPhishingCampaign

from sos_phishing.utils import generate_random_id

class LaunchNewPhishingCampaignView(LoginRequiredMixin, View):
    template_name = 'launch_phishing_campaign/launch_phishing_campaign.html'
    login_url = 'login'

    def get(self, request):
        breadcrumb_pages = [
            { 'label': 'New Campaign', 'url': '' }
        ]
        return render(request, self.template_name, context={
            'breadcrumb_pages': breadcrumb_pages,
            'form': LaunchPhishingCampaign
        })
    
    def post(self, request):
        form = LaunchPhishingCampaign(request.POST)

        if form.is_valid():
            # Récupérer le client associé à l'utilisateur
            client = getattr(request.user, 'client', None)
            if not client:
                messages.error(request, "No client associated with the current user.")
                return redirect('launch_phishing_campaign')

            # Collect form data
            name = form.cleaned_data['name']
            type = form.cleaned_data['type']
            mode = next((m[0] for m in Campaign.MODES if m[0] == 'manual'), None)
            expected_signaling = form.cleaned_data['expected_signaling']
            compromise_type = form.cleaned_data['compromise_type']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            description = form.cleaned_data.get('description', '')
            targets = form.cleaned_data['targets']

            # Create the campaign using the overridden save method
            campaign = Campaign(
                name=name,
                type=type,
                mode=mode,
                expected_signaling=expected_signaling,
                compromise_type=compromise_type,
                start_date=start_date,
                end_date=end_date,
                description=description,
                url_id=generate_random_id()
            )

            # Call the overridden save method with targets_list
            campaign.save(targets_list=list(targets), request=request)
            campaign.clients.add(client)

            # Success message and redirection
            messages.success(request, f"Campaign '{name}' created successfully.")
            return redirect('projects_dashboard')

        # If the form is invalid, display error messages
        messages.error(request, "Please correct the errors in the form.")
        return redirect('launch_phishing_campaign')
