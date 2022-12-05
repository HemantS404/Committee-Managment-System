from django.db import models
from Committee.models import *
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
 

class User(AbstractBaseUser):
    Department = models.CharField(max_length=20, help_text='Enter your Deparment')
    First_name = models.CharField(max_length=20, help_text='Enter your First name')
    Last_name = models.CharField(max_length=20, help_text='Enter your Last name')
    date_of_birth = models.DateField(help_text='Enter your Date of Birth')
    phone = PhoneNumberField(null=False, blank=False, unique=True, help_text='Enter Phone Number')
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        help_text='Enter your Email',
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.First_name+' '+self.Last_name+', '+self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Guide(models.Model):
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name = 'Guide_Committee')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'Guide_User')
    designation = models.CharField(max_length=20, help_text='Enter your Designation')
    department = models.CharField(max_length=20, help_text='Enter your deparment')
    def __str__(self):
        return self.user.First_name +' '+ self.user.Last_name +", "+ self.user.email
    class Meta:
        unique_together = ('user', 'committee')

class Core(models.Model):
    def positionValidator(self):
        pos = [x['id'] for  x in list(Position.objects.filter( Position_for = 'Core').values())]
        if self in pos:
             return self
        else:
            raise ValidationError("Invalid Inputs")

    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name = 'Core_Committee')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'Core_User')
    SAPID = models.PositiveBigIntegerField()
    position = models.ForeignKey(Position,  on_delete=models.CASCADE, related_name = 'Core_Position', validators = [ positionValidator ])
    department = models.CharField(max_length=20, help_text='Enter your deparment')
    def __str__(self):
        return self.user.First_name +' '+ self.user.Last_name +", "+ self.user.email
    class Meta:
        unique_together = ('user', 'committee', 'position')

class CoCom(models.Model):
    def positionValidator(value):
        pos = [x['id'] for  x in list(Position.objects.filter(Position_for = 'CoCom').values())]
        print(pos)
        print(value)
        if value in pos:
             return value
        else:
            raise ValidationError("Invalid Inputs")
    
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name = 'CoCom_Committee')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'CoCom_User')
    SAPID = models.PositiveBigIntegerField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name = 'CoCom_Position', validators = [ positionValidator ])
    department = models.CharField(max_length=20, help_text='Enter your deparment')
    def __str__(self):
        return self.user.First_name +' '+ self.user.Last_name  +", "+ self.user.email
    class Meta:
        unique_together = ('user', 'committee', 'position')
