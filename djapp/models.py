from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

from django_extensions.db.models import TimeStampedModel
import jsonfield


class Institute(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='institute_pics', blank=True)
    email = models.EmailField(max_length=70, blank=True)
    phone_regex = RegexValidator(
        regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[phone_regex], max_length=17)
    brochure = models.FileField(upload_to='picture')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class Branch(TimeStampedModel):
    institute_name = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='branch_institute')
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, blank=True, null=True)
    logo = models.ImageField(upload_to='branch_pics')
    email = models.EmailField(max_length=70, blank=True)
    address = models.CharField(max_length=70)
    phone_regex = RegexValidator(
        regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[phone_regex], max_length=17)
    brochure = models.FileField(upload_to='branch_pics')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'


class UserProfileInfo(TimeStampedModel):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=10, unique=True)
    mobile = models.CharField(max_length=10, null=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=(('male', 'Male'), ('female', 'Female')), max_length=30, null=True, blank=True)
    course = models.CharField(choices=(('btech', 'B Tech'), ('mba', 'MBA'),
                                       ('msc', 'MSC'), ('bca', 'BCA')), max_length=30)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_user')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'UserProfileInfo'
        verbose_name_plural = 'UserProfileInfo'


class Fee(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class FeePaid(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fee_user')
    paid_fee = models.ForeignKey(Fee, on_delete=models.CASCADE, related_name='fee_name')

    class Meta:
        verbose_name = 'FeesPaid'
        verbose_name_plural = 'FeesPaid'


class Orders(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user')
    name = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_id = models.CharField(max_length=100)
    fees_charged = models.TextField()
    razorpay_dump = jsonfield.JSONField()

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return self.name


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
