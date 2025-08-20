from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('moradia', 'Moradia'),
    ('alimentação', 'Alimentação'),
    ('transporte', 'Transporte'),
    ('lazer', 'Lazer'),
    ('saúde', 'Saúde'),
    ('investimentos', 'Investimentos'),
    ('outros', 'Outros'),
]


class Expense(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=25, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.category} - {self.amount}"
