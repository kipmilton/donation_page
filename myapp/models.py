from django.db import models
from django.core.validators import RegexValidator

# Validator to allow only letters and spaces
only_letters_validator = RegexValidator(
    regex=r'^[A-Za-z ]+$',
    message="Only letters and spaces are allowed."
)

class StudentApplication(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[only_letters_validator]  
    )
    age = models.IntegerField()
    school = models.CharField(
        max_length=200,
        validators=[only_letters_validator]  
    )
    student_class = models.CharField(max_length=50)
    guardian_phone = models.CharField(max_length=15)
    annual_cost = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_sponsored = models.BooleanField(default=False)
    supportive_documents = models.FileField(upload_to='supportive_documents/', null=True, blank=True)

    @property
    def balance(self):
        return self.annual_cost - self.amount_paid

    def update_sponsorship_status(self):
        if self.amount_paid >= self.annual_cost:
            self.is_sponsored = True
        else:
            self.is_sponsored = False
        self.save()

    def __str__(self):
        return self.name


class SponsorSelection(models.Model):
    student = models.ForeignKey(StudentApplication, on_delete=models.CASCADE)
    sponsor_name = models.CharField(
        max_length=100,
        validators=[only_letters_validator] 
    )
    sponsor_email = models.EmailField()
    amount_contributed = models.DecimalField(max_digits=10, decimal_places=2)
    date_selected = models.DateTimeField(auto_now_add=True)
    payment_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sponsor_name} -> {self.student.name} (Ksh. {self.amount_contributed})"