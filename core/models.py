from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date
# =========================
# HOUSEHOLD MODEL
# =========================




class Household(models.Model):

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Shifted', 'Shifted'),
    ]

    household_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        editable=False
    )

    locality = models.CharField(max_length=100)

    house_number = models.CharField(max_length=50)

    head_name = models.CharField(max_length=100)


    GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    registration_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Active'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = ['locality', 'house_number']
        ordering = ['-created_at']

    def save(self, *args, **kwargs):

        if not self.household_id:

            last_household = Household.objects.order_by('id').last()

            if last_household and last_household.household_id:
                last_id = int(last_household.household_id[2:]) + 1
            else:
                last_id = 1

            self.household_id = f'HH{last_id:03d}'

        super().save(*args, **kwargs)

     # FIXED HERE
    def __str__(self):
        return f"{self.household_id} - {self.head_name}"
# =========================
# MEMBER MODEL
# =========================

class Member(models.Model):

    household = models.ForeignKey(
        Household,
        on_delete=models.CASCADE,
        related_name='members'
    )

    # AUTO MEMBER ID
    member_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        editable=False
    )

    # Basic Info
    name = models.CharField(max_length=100)

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    dob = models.DateField()

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    RELATIONSHIP_CHOICES = [
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Son', 'Son'),
        ('Daughter', 'Daughter'),
        ('Other', 'Other'),
    ]

    relationship = models.CharField(
        max_length=50,
        #choices=RELATIONSHIP_CHOICES
    )

    # Spiritual Details
    baptism_status = models.BooleanField(default=False)

    baptism_date = models.DateField(
        blank=True,
        null=True
    )

    confirmation_status = models.BooleanField(default=False)

    MEMBERSHIP_CHOICES = [
        ('Believer', 'Believer'),
        ('Catechumen', 'Catechumen'),
        ('Visitor', 'Visitor'),
    ]

    membership_status = models.CharField(
        max_length=20,
        choices=MEMBERSHIP_CHOICES
    )

    # Additional Fields
    qualification = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    occupation = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    MARITAL_CHOICES = [
    ('Unmarried', 'Unmarried'),
    ('Married', 'Married'),
    ('Widowed', 'Widowed'),
    ('Divorced', 'Divorced'),
    ('Separated', 'Separated'),
]

    marital_status = models.CharField(
        max_length=20,
        choices=MARITAL_CHOICES,
        blank=True,
        null=True
    )

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    blood_group = models.CharField(
        max_length=5,
        choices=BLOOD_GROUP_CHOICES,
        blank=True,
        null=True
    )

    skills = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    # Status
    is_deceased = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # AUTO MEMBER ID GENERATION
    def save(self, *args, **kwargs):

        if not self.member_id:

            last_member = Member.objects.order_by('id').last()

            if last_member and last_member.member_id:
                last_id = int(last_member.member_id[3:]) + 1
            else:
                last_id = 1

            self.member_id = f"MEM{last_id:03d}"

        super().save(*args, **kwargs)

    # AUTO AGE CALCULATION
    @property
    def age(self):

        from datetime import date

        today = date.today()

        return today.year - self.dob.year - (
            (today.month, today.day) <
            (self.dob.month, self.dob.day)
        )

    def __str__(self):
        return f"{self.member_id} - {self.name}"


# =========================
# DEATH RECORD MODEL
# =========================


class DeathRecord(models.Model):

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE
    )

    date_of_death = models.DateField()

    cause_of_death = models.TextField(
        blank=True,
        null=True
    )

    funeral_date = models.DateField(
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    death_certificate = models.FileField(
        upload_to='death_certificates/',
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ['member']

    def save(self, *args, **kwargs):

        self.member.is_deceased = True
        self.member.is_active = False

        self.member.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.member.name} - {self.date_of_death}"


# =========================
# BIRTH RECORD MODEL
# =========================
    

class BirthRecord(models.Model):

    household = models.ForeignKey(
        Household,
        on_delete=models.CASCADE,
        related_name='births'
    )

    member = models.OneToOneField(
        Member,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Baby Name
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    dob = models.DateField()

    # Parents
    father_name = models.CharField(
        max_length=100
    )

    mother_name = models.CharField(
        max_length=100
    )

    father_phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    mother_phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    RELATIONSHIP_CHOICES = [
        ('Son', 'Son'),
        ('Daughter', 'Daughter'),
        ('Other', 'Other'),
    ]

    relationship = models.CharField(
        max_length=50,
        choices=RELATIONSHIP_CHOICES
    )

    # Spiritual
    baptism_status = models.BooleanField(
        default=False
    )

    # Certificate
    birth_certificate = models.FileField(
        upload_to='birth_certificates/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = (
            'household',
            'name',
            'dob',
            'father_name',
            'mother_name'
        )

    @property
    def age(self):

        today = date.today()

        if self.dob > today:
            return 0

        return today.year - self.dob.year - (
            (today.month, today.day) <
            (self.dob.month, self.dob.day)
        )

    @property
    def baby_name(self):

        if self.name:
            return self.name

        return f"B/O {self.mother_name}"

    def clean(self):

        if self.dob > date.today():

            raise ValidationError(
                "Date of birth cannot be future date."
            )

    def __str__(self):

        return self.baby_name



    



class User(AbstractUser):

    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Pastor', 'Pastor'),
        ('Operator', 'Operator'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='Operator'
    )
    



# =========================
# OFFERING CATEGORY MODEL
# =========================

class OfferingCategory(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# =========================
# OFFERING MODEL
# =========================

class Offering(models.Model):

    PAYMENT_METHODS = (
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
        ('Bank', 'Bank'),
    )

    category = models.ForeignKey(
        OfferingCategory,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # NEW FIELD
    given_by = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    service_date = models.DateField()

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.category} - {self.amount}"
    



class SiteSettings(models.Model):

    church_name = models.CharField(
        max_length=200,
        default="Church CMS"
    )

    church_logo = models.ImageField(
        upload_to='site_logo/'
    )

    def __str__(self):
        return self.church_name