from django.db import models

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