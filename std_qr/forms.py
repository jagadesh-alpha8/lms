from django import forms
from .models import Registration


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            'full_name', 'college_name', 'college_code', 'branch_department', 'year_of_study',
            'email_address', 'mobile_number', 'preferred_learning_domain', 'preferred_learning_domain_other',
            'preferred_mode_of_learning', 'current_skill_level', 'interested_in_internship', 'interested_in_job',
            'previous_internship_experience', 'internship_company_name', 'internship_role', 'internship_duration',
            'internship_skills_gained', 'prior_job_experience', 'job_company_name', 'job_role', 'job_duration',
            'job_skills_gained', 'preferred_career_domain', 'preferred_career_domain_other', 'availability',
            'open_to_remote', 'resume', 'team_name', 'need_mentor_support', 'college_registration_number',
            'naan_mudhalvan_id', 'district', 'project_file', 'communication_consent'
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'college_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your college name'
            }),
            'college_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter college code'
            }),
            'branch_department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: CSE, IT, ECE, Mechanical, Civil, etc.'
            }),
            'year_of_study': forms.Select(attrs={'class': 'form-select'}),
            'email_address': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 XXXXXXXXXX'
            }),
            'preferred_learning_domain': forms.Select(attrs={'class': 'form-select'}),
            'preferred_learning_domain_other': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Specify other domain'
            }),
            'preferred_mode_of_learning': forms.RadioSelect(),
            'current_skill_level': forms.RadioSelect(),
            'interested_in_internship': forms.RadioSelect(),
            'interested_in_job': forms.RadioSelect(),
            'previous_internship_experience': forms.RadioSelect(),
            'internship_company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company/Organisation Name'
            }),
            'internship_role': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Role / Designation'
            }),
            'internship_duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 3 months, 6 months'
            }),
            'internship_skills_gained': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'List key skills gained (Optional)'
            }),
            'prior_job_experience': forms.RadioSelect(),
            'job_company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company/Organisation Name'
            }),
            'job_role': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Role / Designation'
            }),
            'job_duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 1.5 years, 3 years'
            }),
            'job_skills_gained': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'List key skills gained (Optional)'
            }),
            'preferred_career_domain': forms.Select(attrs={'class': 'form-select'}),
            'preferred_career_domain_other': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Specify other career domain'
            }),
            'availability': forms.RadioSelect(),
            'open_to_remote': forms.RadioSelect(),
            'resume': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'team_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter team name (Required only if you already have a team)'
            }),
            'need_mentor_support': forms.RadioSelect(),
            'college_registration_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'REG NO: ________________'
            }),
            'naan_mudhalvan_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'NM ID: ________________'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your district'
            }),
            'project_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'communication_consent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }