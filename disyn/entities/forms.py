from django import forms
from .models import Application, EntityType, Upvote, VisitorApplication

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'entity_type', 'description', 'location', 'email', 'phone', 'website', 'applicant_name', 'applicant_role']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['entity_type'].queryset = EntityType.objects.all()

class UpvoteForm(forms.ModelForm):
    class Meta:
        model = Upvote
        fields = ['name', 'role', 'reason']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name (Optional)'}),
            'role': forms.TextInput(attrs={'placeholder': 'Your Role (Optional)'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Why are you upvoting this entity? (Optional)'}),
        }



class VisitorApplicationForm(forms.ModelForm):
    class Meta:
        model = VisitorApplication
        fields = ['name', 'email', 'phone', 'application_type', 'message', 'cv']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your purpose for the visit or your qualifications for the job/internship'}),
            'cv': forms.FileInput(attrs={'accept': '.pdf,.doc,.docx'})
        }