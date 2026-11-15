from django import forms
from .models import Scheme, SchemeApplication

TW_INPUT = 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500'
TW_INPUT_DARK = 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'

ORGANIZATION_CHOICES = [
    ('', 'Select Organization'),
    ('Ministry of Education', 'Ministry of Education'),
    ('Ministry of Health', 'Ministry of Health'),
    ('Ministry of Housing & Urban Affairs', 'Ministry of Housing & Urban Affairs'),
    ('Ministry of Agriculture', 'Ministry of Agriculture'),
    ('Ministry of Commerce & Industries', 'Ministry of Commerce & Industries'),
    ('Ministry of Rural Development', 'Ministry of Rural Development'),
    ('Ministry of Social Justice & Empowerment', 'Ministry of Social Justice & Empowerment'),
    ('Ministry of MSME', 'Ministry of MSME'),
    ('Ministry of Finance', 'Ministry of Finance'),
    ('Ministry of Women & Child Development', 'Ministry of Women & Child Development'),
    ('Ministry of Labour & Employment', 'Ministry of Labour & Employment'),
    ('Ministry of Tribal Affairs', 'Ministry of Tribal Affairs'),
    ('Ministry of Home Affairs', 'Ministry of Home Affairs'),
    ('Ministry of Railways', 'Ministry of Railways'),
    ('AICTE', 'AICTE'),
    ('Other', 'Other'),
]


class SchemeForm(forms.ModelForm):
    organization = forms.ChoiceField(
        choices=ORGANIZATION_CHOICES,
        widget=forms.Select(attrs={'class': TW_INPUT_DARK}),
    )

    class Meta:
        model = Scheme
        fields = [
            'name', 'description', 'category', 'organization',
            'min_age', 'max_age', 'max_income',
            'eligible_genders', 'eligible_categories', 'min_education', 'status',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': TW_INPUT_DARK, 'placeholder': 'Scheme Name'}),
            'description': forms.Textarea(attrs={'class': TW_INPUT_DARK, 'rows': 4, 'placeholder': 'Scheme Description'}),
            'category': forms.Select(attrs={'class': TW_INPUT_DARK}),
            'min_age': forms.NumberInput(attrs={'class': TW_INPUT_DARK, 'placeholder': 'Minimum Age'}),
            'max_age': forms.NumberInput(attrs={'class': TW_INPUT_DARK, 'placeholder': 'Maximum Age'}),
            'max_income': forms.NumberInput(attrs={'class': TW_INPUT_DARK, 'placeholder': 'Max Annual Income'}),
            'eligible_genders': forms.TextInput(attrs={'class': TW_INPUT_DARK, 'placeholder': 'e.g. male,female or leave blank for all'}),
            'eligible_categories': forms.TextInput(attrs={'class': TW_INPUT_DARK, 'placeholder': 'e.g. sc,st,obc or leave blank for all'}),
            'min_education': forms.Select(attrs={'class': TW_INPUT_DARK}),
            'status': forms.Select(attrs={'class': TW_INPUT_DARK}),
        }


class SchemeApplicationForm(forms.ModelForm):
    class Meta:
        model = SchemeApplication
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={
                'class': TW_INPUT_DARK,
                'rows': 4,
                'placeholder': 'Explain why you want to apply for this scheme...',
            }),
        }


class SchemeSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': TW_INPUT_DARK,
            'placeholder': 'Search schemes by name or description...',
        }),
    )
    category = forms.ChoiceField(
        required=False,
        choices=[('', 'All Categories')] + list(Scheme._meta.get_field('category').choices),
        widget=forms.Select(attrs={'class': TW_INPUT_DARK}),
    )
