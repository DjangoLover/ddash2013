from django import forms
from django.utils.translation import ugettext_lazy as _

from accounts.models import User
from .models import Organization


class OrganizationRegistrationForm(forms.ModelForm):

    class Meta:
        model = Organization


class OwnerRegistrationForm(forms.ModelForm):

    password1 = forms.CharField(
        label=_(u'Password'), widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label=_(u'Password confirmation'), widget=forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = ['email', 'full_name', 'login']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                _(u"The two password fields didn't match.")
            )
        return password2

    def save(self, commit=True):
        user = super(OwnerRegistrationForm, self).save(commit=commit)
        user.email = User.objects.normalize_email(user.email)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class InviteForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['full_name', 'login', 'email']

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization')
        super(InviteForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = self.organization.members.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError(_(u'This email already registered'))
        return email

    def save(self, commit=True):
        user = super(InviteForm, self).save(commit=False)
        user.organization = self.organization
        user.set_unusable_password()
        if commit:
            user.save()
        return user


class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ['name']


class OrganisationLogoForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ['logo']
