# forms.py
from django import forms
from .models import StudentApplication

class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentApplication
        fields = ['name', 'age', 'school', 'student_class', 'guardian_phone', 'annual_cost', 'supportive_documents']
