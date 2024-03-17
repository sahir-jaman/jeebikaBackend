from django.db import models


class GenderStatus(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    UNKNOWN = "UNKNOWN", "Unknown"
    OTHER = "OTHER", "Other"
    
    
class UserType(models.TextChoices):
    APPLICANT = "APPLICANT", "Applicant"
    EMPLOYER = "EMPLOYER", "Employer"
    

class CompanySize(models.TextChoices):
    ONETOFIFTY = '1-50', '1-50'
    FIFTYONETOHUNDRED = '51-100', '51-100'
    ONETOHUNDRED = '101-200', '101-200'
    TWOHUNDREDONETOFIVEHUNDRED = '201-500', '201-500'
    FIVEHUNDREDONETOTHOUSAND = '501-1000', '501-1000'
    THOUSANDONETOTWOTHOUSAND = '1001-2000', '1001-2000'
    TWOHUNDREDONETOFIVETHOUSAND = '2001-5000', '2001-5000'
    FIVETHOUSANDONEPLUS = '5001+' , '5001+'

    
    
    