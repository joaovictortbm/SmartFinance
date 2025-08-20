from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICES = [
    ('salario', 'Salario'),
    ('negócios', 'Negócios'),
    ('investmento', 'Investmento'),
    ('outros', 'Outros'),
]


class Income(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='incomes')
    amount = models.DecimalField(max_digits=25, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.category} - {self.amount}"
