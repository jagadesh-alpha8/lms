from django.db import models
from django.core.validators import FileExtensionValidator


class Registration(models.Model):
    """
    Main model for Skill Development Program Registration
    Handles Course, Internship/Job Survey, and Hackathon Registration
    """
    
    # Section 1: Basic Information
    college_name = models.CharField(max_length=200, verbose_name="College Name")
    branch_of_study = models.CharField(max_length=100, verbose_name="Branch of Study")
    
    YEAR_CHOICES = [
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
        ('5th Year', '5th Year'),
    ]
    current_year = models.CharField(max_length=20, choices=YEAR_CHOICES, verbose_name="Current Year")
    
    # Course Section
    interested_in_course = models.BooleanField(default=False, verbose_name="Interested in FREE course with certification")
    
    COURSE_DOMAIN_CHOICES = [
        ('Web Development', 'Web Development'),
        ('Data Science', 'Data Science'),
        ('Artificial Intelligence / Machine Learning', 'Artificial Intelligence / Machine Learning'),
        ('Cybersecurity', 'Cybersecurity'),
        ('Cloud Computing', 'Cloud Computing'),
        ('Mobile App Development', 'Mobile App Development'),
        ('UI/UX Design', 'UI/UX Design'),
        ('Other', 'Other'),
    ]
    preferred_course_domain = models.CharField(
        max_length=100, 
        choices=COURSE_DOMAIN_CHOICES, 
        blank=True, 
        null=True,
        verbose_name="Preferred Course Domain"
    )
    
    LEARNING_MODE_CHOICES = [
        ('Online (Live)', 'Online (Live)'),
        ('Online (Recorded)', 'Online (Recorded)'),
        ('Hybrid', 'Hybrid'),
    ]
    preferred_learning_mode = models.CharField(
        max_length=50, 
        choices=LEARNING_MODE_CHOICES, 
        blank=True, 
        null=True,
        verbose_name="Preferred Mode of Learning"
    )
    
    SKILL_LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    current_skill_level = models.CharField(
        max_length=20, 
        choices=SKILL_LEVEL_CHOICES, 
        blank=True, 
        null=True,
        verbose_name="Current Skill Level"
    )
    
    # Section 2: Internship & Job
    has_previous_internship = models.BooleanField(default=False, verbose_name="Previous internship experience")
    internship_duration = models.TextField(blank=True, null=True, verbose_name="Total duration of previous internship")
    internship_roles = models.TextField(blank=True, null=True, verbose_name="Previous internship role(s) or domain(s)")
    internship_skills_gained = models.TextField(blank=True, null=True, verbose_name="Key skills from internship")
    
    currently_doing_internship = models.BooleanField(default=False, verbose_name="Currently pursuing internship")
    current_internship_company = models.CharField(max_length=200, blank=True, null=True, verbose_name="Current internship company")
    current_internship_role = models.CharField(max_length=200, blank=True, null=True, verbose_name="Current internship role")
    current_internship_duration = models.TextField(blank=True, null=True, verbose_name="Duration in current internship")
    
    has_previous_job = models.BooleanField(default=False, verbose_name="Previous job experience")
    job_duration = models.TextField(blank=True, null=True, verbose_name="Total duration of previous job")
    job_roles = models.TextField(blank=True, null=True, verbose_name="Previous job role(s) or domain(s)")
    job_skills_gained = models.TextField(blank=True, null=True, verbose_name="Key skills from job")
    
    currently_employed = models.BooleanField(default=False, verbose_name="Currently employed")
    current_job_company = models.CharField(max_length=200, blank=True, null=True, verbose_name="Current company")
    current_job_role = models.CharField(max_length=200, blank=True, null=True, verbose_name="Current job role")
    current_job_duration = models.TextField(blank=True, null=True, verbose_name="Duration in current job")
    
    OPPORTUNITY_CHOICES = [
        ('Internship', 'Internship'),
        ('Job', 'Job'),
        ('Both', 'Both'),
    ]
    interested_in_opportunities = models.CharField(
        max_length=20, 
        choices=OPPORTUNITY_CHOICES, 
        blank=True, 
        null=True,
        verbose_name="Interested in opportunities"
    )
    
    ROLE_CHOICES = [
        ('Software Developer', 'Software Developer'),
        ('Data Analyst', 'Data Analyst'),
        ('AI / ML Engineer', 'AI / ML Engineer'),
        ('Cybersecurity Analyst', 'Cybersecurity Analyst'),
        ('Cloud Engineer', 'Cloud Engineer'),
        ('UI/UX Designer', 'UI/UX Designer'),
        ('Other', 'Other'),
    ]
    preferred_role = models.CharField(
        max_length=50, 
        choices=ROLE_CHOICES, 
        blank=True, 
        null=True,
        verbose_name="Preferred Role / Domain"
    )
    
    AVAILABILITY_CHOICES = [
        ('Immediate', 'Immediate'),
        ('Within 1–3 months', 'Within 1–3 months'),
        ('After course completion', 'After course completion'),
    ]
    availability = models.CharField(
        max_length=50, 
        choices=AVAILABILITY_CHOICES, 
        blank=True, 
        null=True,
        verbose_name="Availability"
    )
    
    open_to_remote = models.BooleanField(default=False, verbose_name="Open to remote opportunities")
    resume = models.FileField(
        upload_to='resumes/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        verbose_name="Resume Upload"
    )
    
    # Section 3: Hackathon Registration
    interested_in_hackathon = models.BooleanField(default=False, verbose_name="Interested in Hackathon")
    has_hackathon_experience = models.BooleanField(default=False, verbose_name="Previous Hackathon Experience")
    
    HACKATHON_MODE_CHOICES = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
        ('Hybrid', 'Hybrid'),
    ]
    preferred_hackathon_mode = models.CharField(
        max_length=20, 
        choices=HACKATHON_MODE_CHOICES, 
        blank=True, 
        null=True,
        verbose_name="Preferred Hackathon Mode"
    )
    
    participant_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Participant Name")
    participant_email = models.EmailField(blank=True, null=True, verbose_name="Participant Email")
    
    TEAM_PREFERENCE_CHOICES = [
        ('Already have a team', 'Already have a team'),
        ('Want to join a team', 'Want to join a team'),
        ('Solo participant', 'Solo participant'),
    ]
    team_preference = models.CharField(
        max_length=50, 
        choices=TEAM_PREFERENCE_CHOICES, 
        blank=True, 
        null=True,
        verbose_name="Team Preference"
    )
    
    team_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Team Name")
    participant_mobile = models.CharField(max_length=15, blank=True, null=True, verbose_name="Participant Mobile Number")
    consent = models.BooleanField(default=False, verbose_name="Consent to be contacted")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Registration"
        verbose_name_plural = "Registrations"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.college_name} - {self.branch_of_study} ({self.current_year})"