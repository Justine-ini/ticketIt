from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.TextField(blank=True, null=True)
  Address = models.CharField(max_length=100, blank=True, null=True)
  birth_date = models.DateField(blank=True, null=True)
  
  def __str__(self):
    return self.user.username
  

class Sector(models.Model):
  SECTOR_CHOICES = (
    ('retail', 'Retail'),
    ('banking', 'Banking'),
    ('telecom', 'Telecom'),
    ('healthcare', 'Healthcare'),
    ('utilities', 'Utilities'),
  )

  name = models.CharField(
    max_length=50,
    choices=SECTOR_CHOICES,
    unique=True
  )
  # company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='sectors')

  def __str__(self):
    return dict(self.SECTOR_CHOICES).get(self.name, self.name)
  
class Company(models.Model):
  name = models.CharField(max_length=100)
  sector = models.ForeignKey(Sector, on_delete=models.DO_NOTHING, related_name='company', null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name = "Account Company"
    verbose_name_plural = "Companies"

  def __str__(self):
    return f"{self.name}"

class Ticket(models.Model):
  title = models.CharField(max_length=100, null=True)
  user_email = models.EmailField(max_length=100, null=True)  
  recipient_email = models.EmailField(max_length=100, null=True)
  company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='ticket')
  sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='ticket')
  description = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  status = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.title} - {self.company.name} - {self.description[:30]}"