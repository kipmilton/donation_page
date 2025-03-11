# models.py
from django.db import models

class StudentApplication(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    school = models.CharField(max_length=200)
    student_class = models.CharField(max_length=50)
    guardian_phone = models.CharField(max_length=15)
    annual_cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_sponsored = models.BooleanField(default=False)
    supportive_documents = models.FileField(upload_to='supportive_documents/', null=True, blank=True)

    def __str__(self):
        return self.name

class SponsorSelection(models.Model):
    student = models.ForeignKey(StudentApplication, on_delete=models.CASCADE)
    sponsor_name = models.CharField(max_length=100)
    sponsor_email = models.EmailField()
    date_selected = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor_name} -> {self.student.name}"
