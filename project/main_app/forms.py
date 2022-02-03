from django import forms

from main_app.models import Case, CasePhoto, Comment


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ('type', 'place', 'description')
        labels = {
            'type': 'Rodzaj zgłoszenia',
            'place': 'Lokalizacja',
            'description': 'Opis'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8, 'cols': 70}),
        }

    def __init__(self, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs[
            'placeholder'] = 'Podaj jak najwięcej szczegółów: wygląd i zachowanie zwierzęcia, ' \
                             'godzinę i datę znalezenia/zaginięcia itp.'


class PhotoForm(forms.Form):
    photos = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                              required=False, label='Dodaj zdjęcia (opcjonalnie)')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': ''
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8, 'cols': 70}),
        }
