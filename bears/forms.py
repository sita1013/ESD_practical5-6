from django import forms
from .models import Bear

class BearForm (forms.ModelForm):
    class Meta:
        model = Bear
        fields = ('bearID', 'pTT_ID', 'capture_lat', 'capture_long', 'sex','age_class','ear_applied') 