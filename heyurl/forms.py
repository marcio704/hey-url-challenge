from django.forms import ModelForm
from heyurl.models import Url


class UrlValidationForm(ModelForm):
    class Meta:
        model = Url
        fields = ['original_url']
