from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from common.models import BaseModelWithUID
from common.choices import GenderStatus
from accountio.models import User



class skill_list(BaseModelWithUID):
    skill_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.skill_name

# Create your models here.
class Applicant(AbstractBaseUser, BaseModelWithUID):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='applicant')
    gender = models.CharField(max_length=10, choices=GenderStatus.choices, default=GenderStatus.UNKNOWN)
    skill_title = models.ForeignKey(skill_list, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username