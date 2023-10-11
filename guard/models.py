from django.db import models
from django.contrib.auth.models import AbstractUser, User



class SafeguardLead(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Therapist(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    # avatar?
    phone = models.CharField(max_length=20)
    safeguard_lead = models.ForeignKey(SafeguardLead, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_status(self):
        return 'In Appointment'



class Client(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    email = models.EmailField()
    notes = models.TextField()

    def __str__(self):
        return self.name


class Appointment(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    app_type = models.CharField(max_length=20, choices=[(i, i) for i in ['Virtual', 'Office', 'Home']])
    checked_in = models.BooleanField(null=True)
    checked_out = models.BooleanField(null=True)
    check_in_time = models.DateTimeField(null=True)
    check_out_time = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.therapist.name} - {self.client.name} - {self.start_time}"

