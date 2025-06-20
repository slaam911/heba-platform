from django import forms
from .models import BloodRequest
from users.models import City
from collections import defaultdict

class BloodRequestForm(forms.ModelForm):
    terms = forms.BooleanField(
        label="أتعهد بأن جميع البيانات المدخلة صحيحة وتحت مسؤوليتي",
        error_messages={'required': 'يجب الموافقة على التعهد لإرسال الطلب.'}
    )
    
    class Meta:
        model = BloodRequest
        fields = [
            'patient_name', 'medical_file_number', 'hospital_name', 'city',
            'blood_type', 'blood_component', 'patient_age', 'patient_gender',
            'units_needed', 'is_critical', 'contact_number', 'additional_info'
        ]
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المريض'}),
            'medical_file_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الملف الطبي'}),
            'hospital_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المستشفى'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'blood_type': forms.Select(attrs={'class': 'form-select'}),
            'blood_component': forms.Select(attrs={'class': 'form-select'}),
            'patient_age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'عمر المريض'}),
            'patient_gender': forms.Select(attrs={'class': 'form-select'}),
            'units_needed': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'عدد الوحدات المطلوبة'}),
            'is_critical': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم للتواصل'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'وصف إضافي للحالة', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ترتيب المدن حسب المنطقة وتجميعها في مجموعات
        from users.models import REGION_CHOICES
        grouped_cities = defaultdict(list)
        for city in City.objects.filter(is_active=True).order_by('region', 'name'):
            grouped_cities[city.get_region_display()].append((city.id, city.name))
        choices = []
        for region_code, region_name in REGION_CHOICES:
            if grouped_cities[region_name]:
                choices.append((region_name, grouped_cities[region_name]))
        self.fields['city'].choices = [('', '---------')] + choices
        
        # إضافة رسائل الخطأ المخصصة
        self.fields['patient_name'].error_messages = {'required': 'يرجى إدخال اسم المريض'}
        self.fields['medical_file_number'].error_messages = {'required': 'يرجى إدخال رقم الملف الطبي'}
        self.fields['hospital_name'].error_messages = {'required': 'يرجى إدخال اسم المستشفى'}
        self.fields['city'].error_messages = {'required': 'يرجى اختيار المدينة'}
        self.fields['blood_type'].error_messages = {'required': 'يرجى اختيار فصيلة الدم'}
        self.fields['blood_component'].error_messages = {'required': 'يرجى اختيار نوع الدم المطلوب'}
        self.fields['patient_age'].error_messages = {'required': 'يرجى إدخال عمر المريض'}
        self.fields['patient_gender'].error_messages = {'required': 'يرجى اختيار جنس المريض'}
        self.fields['units_needed'].error_messages = {'required': 'يرجى إدخال عدد الوحدات المطلوبة'}
        self.fields['contact_number'].error_messages = {'required': 'يرجى إدخال رقم للتواصل'}
    
    # حذف دالة clean_medical_report لأنها لم تعد مطلوبة 