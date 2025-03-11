# from django.contrib import admin

# # Register your models here.
# # admin.py
# from django.contrib import admin
# from django.http import HttpResponse
# import csv
# from .models import StudentApplication, SponsorSelection

# class StudentApplicationAdmin(admin.ModelAdmin):
#     list_display = ('name', 'age', 'school', 'student_class', 'guardian_phone', 'annual_cost', 'is_sponsored', 'supportive_documents')
#     list_filter = ('is_sponsored',)
#     search_fields = ('name', 'school')

#     # Add an export function to export the table data to CSV
#     actions = ['export_to_csv']

#     def export_to_csv(self, request, queryset):
#         # Create a response object with CSV content type
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="student_applications.csv"'

#         writer = csv.writer(response)
#         writer.writerow(['Name', 'Age', 'School', 'Class', 'Guardian Phone', 'Annual Cost', 'Sponsored', 'Supportive Documents'])

#         # Write each student application as a row in the CSV file
#         for student in queryset:
#             writer.writerow([student.name, student.age, student.school, student.student_class, student.guardian_phone, student.annual_cost, student.is_sponsored, student.supportive_documents.url if student.supportive_documents else ""])

#         return response

#     export_to_csv.short_description = "Export selected students to CSV"

# # Register models with admin
# admin.site.register(StudentApplication, StudentApplicationAdmin)
# admin.site.register(SponsorSelection)


# admin.py
from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import StudentApplication, SponsorSelection

class StudentApplicationAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ('name', 'age', 'school', 'student_class', 'guardian_phone', 'annual_cost', 'is_sponsored', 'supportive_documents')
    
    # Add filtering by sponsorship status
    list_filter = ('is_sponsored',)
    
    # Allow searching by name and school
    search_fields = ('name', 'school')

    # Add action to export the selected students to a CSV file
    actions = ['export_to_csv']

    def export_to_csv(self, request, queryset):
        # Generate a CSV response with student data
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="student_applications.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Age', 'School', 'Class', 'Guardian Phone', 'Annual Cost', 'Sponsored', 'Supportive Documents'])

        # Write each student's information as a row in the CSV
        for student in queryset:
            writer.writerow([
                student.name,
                student.age,
                student.school,
                student.student_class,
                student.guardian_phone,
                student.annual_cost,
                student.is_sponsored,
                student.supportive_documents.url if student.supportive_documents else ""
            ])

        return response

    # Set the display name for the export action
    export_to_csv.short_description = "Export selected students to CSV"

# Register models in the admin site
admin.site.register(StudentApplication, StudentApplicationAdmin)
admin.site.register(SponsorSelection)
