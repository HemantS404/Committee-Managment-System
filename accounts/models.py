from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError

class Committee(models.Model):
    Committee_name = models.CharField(max_length=20, help_text='Enter name of the committee', unique=True)
    Committee_Department = models.CharField(max_length=20, help_text='Enter deparment of the committee')
    Committee_Logo = models.ImageField(upload_to='CommitteLogo/')
    Committee_date_of_establishment = models.DateField()
    def __str__(self):
        return self.Committee_name

class Position(models.Model):

    position_for_chocies = [('Core', 'Core'), ('CoCom', 'CoCom')]

    Committee = models.ForeignKey(Committee, on_delete = models.CASCADE, related_name = 'Position_Committee')
    Position_name =  models.CharField(max_length=20, help_text='Enter the name of position')
    Position_for = models.CharField(max_length=20,choices=position_for_chocies)
    class Meta:
        unique_together = ('Committee', 'Position_name', 'Position_for')

    def __str__(self):
        return self.Committee.Committee_name+"'s "+self.Position_name  

class User(AbstractBaseUser):
    First_name = models.CharField(max_length=20, help_text='Enter your First name')
    Last_name = models.CharField(max_length=20, help_text='Enter your Last name')
    date_of_birth = models.DateField(help_text='Enter your Date of Birth')
    phone = PhoneNumberField(null=False, blank=False, unique=True, help_text='Enter Phone Number')
    department = models.CharField(max_length=20, help_text='Enter your deparment')
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        help_text='Enter your Email',
    )
    email_token =  models.CharField(max_length=250, null=True, blank=True)
    phone_otp = models.IntegerField(null=True, blank=True)
    password_reset_token = models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

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
    
    def is_verify(self):
        return (self.is_email_verified and self.is_phone_verified)

class Guide(models.Model):
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name = 'Guide_Committee')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'Guide_User')
    designation = models.CharField(max_length=20, help_text='Enter your Designation')
    
    def __str__(self):
        return self.user.First_name +' '+ self.user.Last_name +", "+ self.user.email
    class Meta:
        unique_together = ('user', 'committee')

class Core(models.Model):
    def positionValidator(value):
        pos = [x['id'] for  x in list(Position.objects.filter( Position_for = 'Core').values())]
        if(str(type(value)) == "<class 'accounts.models.Position'>"):
            if value.id in pos:
                return value
            else:
                raise ValidationError("The position is not for Core")
        else:
            if value in pos:
                return value
            else:
                raise ValidationError("The position is not for Core")

    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name = 'Core_Committee')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'Core_User')
    position = models.ForeignKey(Position,  on_delete=models.CASCADE, related_name = 'Core_Position', validators = [ positionValidator ])
    
    def __str__(self):
        return self.user.First_name +' '+ self.user.Last_name +", "+ self.user.email+", "+self.committee.Committee_name+"'s "+self.position.Position_name
    class Meta:
        unique_together = ('user', 'committee', 'position')

class CoCom(models.Model):
    def positionValidator(value):
        pos = [x['id'] for  x in list(Position.objects.filter(Position_for = 'CoCom').values())]
        if(str(type(value)) == "<class 'accounts.models.Position'>"):
            if value.id in pos:
                return value
            else:
                raise ValidationError("The position is not for CoCom")
        else:
            if value in pos:
                return value
            else:
                raise ValidationError("The position is not for CoCom")
    
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name = 'CoCom_Committee')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'CoCom_User')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name = 'CoCom_Position', validators = [ positionValidator ])

    def __str__(self):
        return self.user.First_name +' '+ self.user.Last_name  +", "+ self.user.email+", "+self.committee.Committee_name+"'s "+self.position.Position_name
    class Meta:
        unique_together = ('user', 'committee', 'position')
