from django import forms
from .models import BloodBankUser

class BloodBankUserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تأكيد كلمة المرور', widget=forms.PasswordInput)

    class Meta:
        model = BloodBankUser
        fields = [
            'username', 'email', 'password1', 'password2',
            'bloodbank_name', 'hospital_name', 'region', 'city', 'contact_number',
            'address', 'map_location', 'working_hours', 'special_instructions',
            'manager_name', 'manager_phone', 'manager_email', 'manager_position'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['special_instructions'].initial = 'النوم الكافي لا يقل عن 6 ساعات - أكل وجبة قبل التبرع بمدة ساعة - عدم تناول أدوية'

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'كلمتا المرور غير متطابقتين')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user 