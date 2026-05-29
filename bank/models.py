from django.db import models
from decimal import Decimal
from django.db.models import Sum


# ======================================
# BANK ACCOUNT MODEL
# ======================================

class BankAccount(models.Model):

    account_name = models.CharField(
        max_length=150
    )

    bank_name = models.CharField(
        max_length=150
    )

    account_number = models.CharField(
        max_length=50,
        unique=True
    )

    ifsc_code = models.CharField(
        max_length=20
    )

    opening_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.account_name

    @property
    def total_deposits(self):

        total = self.transactions.filter(
            transaction_type='DEPOSIT'
        ).aggregate(
            total=Sum('amount')
        )['total']

        return total or Decimal('0.00')

    @property
    def total_withdrawals(self):

        total = self.transactions.filter(
            transaction_type='WITHDRAWAL'
        ).aggregate(
            total=Sum('amount')
        )['total']

        return total or Decimal('0.00')

    @property
    def current_balance(self):

        return (
            self.opening_balance +
            self.total_deposits -
            self.total_withdrawals
        )


# ======================================
# BANK TRANSACTION MODEL
# ======================================

class BankTransaction(models.Model):

    TRANSACTION_TYPES = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
    )

    SOURCE_CHOICES = (
        ('OFFERING', 'Offering'),
        ('DONATION', 'Donation'),
    )

    bank_account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    date = models.DateField()

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    # For Deposits
    source = models.CharField(
        max_length=50,
        choices=SOURCE_CHOICES,
        blank=True,
        null=True
    )

    # For Withdrawals
    purpose = models.TextField(
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):

        return (
            f"{self.transaction_type} - "
            f"{self.amount}"
        )