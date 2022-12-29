from django.db import models
from accounts.models import *
# Create your models here.

class Team(models.Model):
    team_name = models.CharField(max_length=20)
    belongs_to = models.ForeignKey(Committee, on_delete=models.CASCADE,related_name='Committee')
    Mentors = models.ManyToManyField(Core)
    Mentee = models.ManyToManyField(CoCom)

    def __str__(self) :
        return self.team_name

class Task(models.Model):
    task_name = models.CharField(max_length = 20)
    team_assign = models.ForeignKey(Team, on_delete= models.CASCADE, related_name='Team')
    assigned_by = models.ForeignKey(Core, on_delete= models.CASCADE, related_name='Core')
    description = models.CharField(max_length=200)
    material = models.FileField(upload_to ='Tasks/')

    def __str__(self):
        return self.task_name

class AssignedTo(models.Model):
    task = models.ForeignKey(Task, on_delete = models.CASCADE, related_name='Task')
    assgined_to = models.ForeignKey(CoCom, on_delete=models.CASCADE, related_name='assigned_to')
    submitted = models.BooleanField(default = False)
    comments = models.CharField(max_length = 200,null=True, blank=True)
    repo_link = models.URLField(null=True, blank=True)
    upload = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.assgined_to.user.First_name +" "+self.assgined_to.user.Last_name+"'s "+self.task.task_name