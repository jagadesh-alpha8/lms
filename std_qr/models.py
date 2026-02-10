from django.db import models
from django.core.validators import FileExtensionValidator


class Registration(models.Model):

    form_title = models.CharField(
        max_length=500,
        verbose_name="Form Title"
    )

    # SECTION 1 – BASIC DETAILS
    full_name = models.CharField(max_length=200)
    college_name = models.CharField(max_length=200)
    college_code = models.CharField(max_length=50)

    branch_department = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    YEAR_CHOICES = [
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('Final Year', 'Final Year'),
    ]

    year_of_study = models.CharField(
        max_length=20,
        choices=YEAR_CHOICES
    )

    email_address = models.EmailField()
    mobile_number = models.CharField(max_length=15)

    # SECTION 2
    LEARNING_DOMAIN_CHOICES = [
        ('Web Development', 'Web Development'),
        ('Data Science', 'Data Science'),
        ('Artificial Intelligence / Machine Learning', 'AI / ML'),
        ('Cybersecurity', 'Cybersecurity'),
        ('Cloud Computing', 'Cloud Computing'),
        ('Mobile App Development', 'Mobile App Development'),
        ('UI/UX Design', 'UI/UX Design'),
        ('Internet of Things (IoT)', 'IoT'),
        ('Other', 'Other'),
    ]

    preferred_learning_domain = models.CharField(
        max_length=100,
        choices=LEARNING_DOMAIN_CHOICES
    )

    preferred_learning_domain_other = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    LEARNING_MODE_CHOICES = [
        ('Online Live', 'Online Live'),
        ('Online Recorded', 'Online Recorded'),
        ('Hybrid Mode', 'Hybrid Mode'),
    ]

    preferred_mode_of_learning = models.CharField(
        max_length=50,
        choices=LEARNING_MODE_CHOICES
    )

    SKILL_LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('No prior knowledge', 'No prior knowledge'),
    ]

    current_skill_level = models.CharField(
        max_length=50,
        choices=SKILL_LEVEL_CHOICES
    )

    # SECTION 3
    INTEREST_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Maybe', 'Maybe'),
    ]

    interested_in_internship = models.CharField(
        max_length=10,
        choices=INTEREST_CHOICES
    )

    interested_in_job = models.CharField(
        max_length=10,
        choices=[('Yes', 'Yes'), ('No', 'No')]
    )

    EXPERIENCE_CHOICES = [
        ('Yes', 'Yes'),
        ('Currently pursuing', 'Currently pursuing'),
        ('No', 'No'),
    ]

    previous_internship_experience = models.CharField(
        max_length=50,
        choices=EXPERIENCE_CHOICES
    )

    internship_company_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    internship_role = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    internship_duration = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    internship_skills_gained = models.TextField(
        blank=True,
        null=True
    )

    prior_job_experience = models.CharField(
        max_length=50,
        choices=EXPERIENCE_CHOICES
    )

    job_company_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    job_role = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    job_duration = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    job_skills_gained = models.TextField(
        blank=True,
        null=True
    )

    CAREER_DOMAIN_CHOICES = [
        ('Software Development', 'Software Development'),
        ('Data Analytics', 'Data Analytics'),
        ('AI / ML', 'AI / ML'),
        ('Cybersecurity', 'Cybersecurity'),
        ('Cloud Computing', 'Cloud Computing'),
        ('UI/UX Design', 'UI/UX Design'),
        ('Core Engineering', 'Core Engineering'),
        ('Other', 'Other'),
    ]

    preferred_career_domain = models.CharField(
        max_length=100,
        choices=CAREER_DOMAIN_CHOICES
    )

    preferred_career_domain_other = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    AVAILABILITY_CHOICES = [
        ('Immediate', 'Immediate'),
        ('Within 1 to 3 months', 'Within 1 to 3 months'),
        ('After course completion', 'After course completion'),
    ]

    availability = models.CharField(
        max_length=50,
        choices=AVAILABILITY_CHOICES
    )

    REMOTE_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Open to Both', 'Open to Both'),
    ]

    open_to_remote = models.CharField(
        max_length=20,
        choices=REMOTE_CHOICES
    )

    resume = models.FileField(
        upload_to="resumes/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])]
    )

    # SECTION 4
    team_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    need_mentor_support = models.CharField(
        max_length=10,
        choices=INTEREST_CHOICES
    )

    college_registration_number = models.CharField(
        max_length=100
    )

    naan_mudhalvan_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    district = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    project_file = models.FileField(
        upload_to="projects/",
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])]
    )

    # SECTION 5
    communication_consent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
