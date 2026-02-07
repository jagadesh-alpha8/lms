from django import forms
from .models import Registration


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['college_name', 'branch_of_study', 'current_year', 
                  'interested_in_course', 'preferred_course_domain', 'preferred_learning_mode', 'current_skill_level',
                  'has_previous_internship', 'internship_duration', 'internship_roles', 'internship_skills_gained',
                  'currently_doing_internship', 'current_internship_company', 'current_internship_role', 'current_internship_duration',
                  'has_previous_job', 'job_duration', 'job_roles', 'job_skills_gained',
                  'currently_employed', 'current_job_company', 'current_job_role', 'current_job_duration',
                  'interested_in_opportunities', 'preferred_role', 'availability', 'open_to_remote', 'resume',
                  'interested_in_hackathon', 'has_hackathon_experience', 'preferred_hackathon_mode',
                  'participant_name', 'participant_email', 'team_preference', 'team_name', 'participant_mobile', 'consent']

        widgets = {
            'college_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your college name'
            }),
            'branch_of_study': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., CSE, ECE, IT'
            }),
            'current_year': forms.Select(attrs={'class': 'form-select'}),
            'interested_in_course': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'preferred_course_domain': forms.Select(attrs={'class': 'form-select'}),
            'preferred_learning_mode': forms.RadioSelect(),
            'current_skill_level': forms.RadioSelect(),
            'has_previous_internship': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'internship_duration': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Please provide detailed information'
            }),
            'internship_roles': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'e.g., Web Development Intern'
            }),
            'internship_skills_gained': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'List key skills'
            }),
            'currently_doing_internship': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'current_internship_company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company name'
            }),
            'current_internship_role': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your role'
            }),
            'current_internship_duration': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Duration'
            }),
            'has_previous_job': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'job_duration': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Total duration'
            }),
            'job_roles': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Previous roles'
            }),
            'job_skills_gained': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Key skills'
            }),
            'currently_employed': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'current_job_company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company name'
            }),
            'current_job_role': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your role'
            }),
            'current_job_duration': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Duration'
            }),
            'interested_in_opportunities': forms.RadioSelect(),
            'preferred_role': forms.Select(attrs={'class': 'form-select'}),
            'availability': forms.RadioSelect(),
            'open_to_remote': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'resume': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'interested_in_hackathon': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'has_hackathon_experience': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'preferred_hackathon_mode': forms.RadioSelect(),
            'participant_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'participant_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'team_preference': forms.RadioSelect(),
            'team_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Team name'
            }),
            'participant_mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 XXXXXXXXXX'
            }),
            'consent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }