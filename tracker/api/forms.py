from django import forms
from .models import Candidate

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["name", "email", "phone_number", "age", "gender"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "trackermodalinput",
                "required": "required",
                "placeholder": "Name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "trackermodalinput",
                "required": "required",
                "placeholder": "Email",
            }),
            "phone_number": forms.TextInput(attrs={
                "class": "trackermodalmetalinput",
                "required": "required",
                "pattern": "[0-9]{10}",
                "placeholder": "Contact number",
                "max_length": 10
        	}),
            "age": forms.IntegerField(attrs={
                "class": "trackermodalmetarinput",
                "required": "required",
                "placeholder": "Age",
                "min": 18,
                "max": 100
            }),
            "gender": forms.Select(attrs={"class": "form-control", "required": "required"}),
        }
