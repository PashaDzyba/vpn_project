from django import forms
from .models import VpnServer, ConnectionLog
from django.core.exceptions import ValidationError
import re



class VpnServerForm(forms.ModelForm):
    class Meta:
        model = VpnServer
        fields = ['name', 'ip_address', 'country', 'city', 'active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DurationField(forms.Field):
    def to_python(self, value):
        # Convert the input to a duration.
        # This is a simplistic parser - you'll want to expand it to handle all cases and validation
        match = re.match(r'(\d+)\s*hour[s]?\s*(\d+)\s*minute[s]?', value, re.IGNORECASE)
        if not match:
            raise ValidationError('Enter a valid duration (e.g., "1 hour 30 minutes").')

        hours, minutes = match.groups()
        return int(hours) * 60 + int(minutes)

    def validate(self, value):
        # Use this method to validate the value
        super().validate(value)


class DataTransferredField(forms.Field):
    def to_python(self, value):
        # Convert the input to a number of megabytes.
        # This parser assumes MB if no unit is provided - expand as needed
        match = re.match(r'(\d+)(MB|GB)?', value, re.IGNORECASE)
        if not match:
            raise ValidationError('Enter a valid amount of data transferred (e.g., "500MB" or "2GB").')

        amount, unit = match.groups()
        amount = int(amount)
        if unit and unit.upper() == 'GB':
            amount *= 1024  # Convert to MB if GB
        return amount

    def validate(self, value):
        # Use this method to validate the value
        super().validate(value)


class ConnectionLogForm(forms.ModelForm):
    duration = DurationField()
    data_transferred = DataTransferredField()

    class Meta:
        model = ConnectionLog
        fields = ['user', 'vpn_server', 'timestamp', 'end_time', 'data_transferred']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'vpn_server': forms.Select(attrs={'class': 'form-control'}),
            'timestamp': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            # 'duration' and 'data_transferred' will use custom widgets based on their custom fields
        }