import django_filters
from .models import Registration
from django.db.models import Q


class RegistrationFilter(django_filters.FilterSet):
    form_title = django_filters.ChoiceFilter(
        label="Form Title",
        choices=[]
    )
    search = django_filters.CharFilter(
        method='filter_search',
        label='Search'
    )
    class Meta:
        model = Registration
        fields = ['form_title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get distinct form titles from DB
        titles = Registration.objects.values_list('form_title', flat=True).distinct()
        self.filters['form_title'].extra['choices'] = [
            (title, title) for title in titles if title
        ]

    def filter_search(self, queryset, name, value):
            return queryset.filter(
                Q(full_name__icontains=value) |
                Q(email_address__icontains=value) |
                Q(mobile_number__icontains=value)
            )       
