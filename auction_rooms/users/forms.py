from django import forms
from django.forms.widgets import HiddenInput
from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import LoginForm, SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm

from auction_rooms.auctions.models import Auction, Favourite
from auction_rooms.users import models


class ARLoginForm(LoginForm):
    error_messages = {
        'account_inactive': _(
            "This account is currently inactive."
        ),
        'email_password_mismatch': _(
            "We didn't recognise that email/password."
        ),
        'username_password_mismatch': _(
            "We didn't recognise that email/password."
        ),
        'username_email_password_mismatch': _(
            "We didn't recognise that email/password."
        )
    }

    def __init__(self, *args, **kwargs):
        super(ARLoginForm, self).__init__(*args, **kwargs)
        self.fields['favourite'] = forms.CharField(
            required=False,
            widget=HiddenInput()
        )

    def login(self, request, redirect_url=None):
        ret = super(ARLoginForm, self).login(request, redirect_url=redirect_url)
        data = self.cleaned_data
        if 'favourite' in data and data['favourite'] != '':
            try:
                Favourite.objects.create(
                    user=self.user,
                    auction=Auction.objects.get(
                        pk=data['favourite']
                    )
                )
            except Auction.DoesNotExist:
                pass
        return ret


class ARSignupForm(SignupForm):
    _USER_TYPE_CHOICES = (
        (models.User.USER_TYPE_GUEST, 'I\'m looking for experiences'),
        (models.User.USER_TYPE_PROVIDER, 'I\'m selling experiences'),
    )
    user_type = forms.ChoiceField(choices=_USER_TYPE_CHOICES)
    phone = forms.CharField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(ARSignupForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            if 'user_type' in kwargs['initial']:
                self.fields['user_type'].widget = forms.widgets.HiddenInput(attrs={
                    'hidden': True
                })
                if kwargs['initial']['user_type'] == models.User.USER_TYPE_GUEST:
                    self.fields['phone'].widget = forms.widgets.HiddenInput(attrs={
                        'hidden': True
                    })
        self.fields['favourite'] = forms.CharField(required=False, widget=HiddenInput())

    def save(self, request):
        user = super(ARSignupForm, self).save(request)
        data = self.cleaned_data
        if 'favourite' in data and data['favourite'] != '':
            try:
                Favourite.objects.create(
                    user=user,
                    auction=Auction.objects.get(
                        pk=data['favourite']
                    )
                )
            except Auction.DoesNotExist:
                pass
        return user


class ARSocialSignupForm(SocialSignupForm):
    _USER_TYPE_CHOICES = (
        (models.User.USER_TYPE_GUEST, 'I\'m looking for experiences'),
        (models.User.USER_TYPE_PROVIDER, 'I\'m selling experiences'),
    )
    user_type = forms.ChoiceField(choices=_USER_TYPE_CHOICES)
    phone = forms.CharField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()
    favourite = forms.CharField(required=False, widget=HiddenInput())

    def __init__(self, *args, **kwargs):
        super(ARSocialSignupForm, self).__init__(*args, **kwargs)
        if 'data' in kwargs and kwargs['data']['user_type'] == models.User.USER_TYPE_PROVIDER:
            self.fields['phone'].required = True

    def save(self, request):
        state = request.session._session_cache[
            'socialaccount_sociallogin'
        ]['state']
        user = super(ARSocialSignupForm, self).save(request)
        if 'auth_params' in state and state['auth_params'] != '':
            try:
                Favourite.objects.create(
                    user=user,
                    auction=Auction.objects.get(
                        pk=state['auth_params']
                    )
                )
            except Auction.DoesNotExist:
                pass
        return user
