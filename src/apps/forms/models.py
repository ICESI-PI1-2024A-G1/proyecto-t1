from django.db import models


# Create your models here.
class FormField(models.Model):
    TYPE_CHOICES = [
        ("text", "Texto"),
        ("number", "Número"),
        ("email", "Correo electrónico"),
        # Otros tipos de campo que desees agregar
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    label = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    col_idx = models.IntegerField()
    row_idx = models.IntegerField()

    def __str__(self):
        return self.label


class ExcelForm(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    excel_file = models.FileField(upload_to="excel_files/")
    form_fields = models.ManyToManyField(FormField)

    def __str__(self):
        return self.name
