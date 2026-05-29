from django.db import models


class Expenditure(models.Model):

    CATEGORY_CHOICES = [
        ('Salary', 'Salary'),
        ('Maintenance', 'Maintenance'),
        ('Program', 'Program'),
        ('Utility', 'Utility'),
        ('Other', 'Other'),
    ]

    PAYMENT_MODE_CHOICES = [
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cheque', 'Cheque'),
        ('UPI', 'UPI'),
    ]

    date = models.DateField()

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField()

    approved_by = models.CharField(max_length=100)

    payment_mode = models.CharField(
        max_length=50,
        choices=PAYMENT_MODE_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"
