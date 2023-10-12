from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone


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
    
    def get_current_status(self):
        """
        Can be in a meeting, meeting in x mins (or hours), or x mins/hours late to check in meeting,
        or likewise for checking out of meeting
        Say up to 10 mins is amber, more than 30 mins is red!
        """
        try:
            appointments = self.appointment_set.all()
            live_appointments = appointments.filter(checked_in=True).exclude(checked_out=True)
            now = timezone.now()
            
            if len(live_appointments):
                # then need to check if checkout time is cause for concern
                app = live_appointments.first()
                diff = (app.end_time - now).total_seconds()
                # 5 mins grace period
                if diff >= 0:
                    return "In a meeting", 0
                elif diff >= -300:
                    return f"{int(-1*diff/60)} mins late to check out", 0
                elif diff >= -600:
                    return f"{int(-1*diff/60)} mins late to check out", 1
                elif diff >= -3600:
                    return f"{int(-1*diff/60)} mins late to check out", 2
                else:
                    hours = int(-1*diff/3600)
                    if hours == 1:
                        return f"1 hour late to check out", 2
                    else:
                        return f"{hours} hours late to check out", 2
            
            # now if no active appointments, check if they are late to start one
            late_appointments = appointments.exclude(checked_in=True).filter(start_time__lt=now)
            if len(late_appointments):
                app = late_appointments.first()
                diff = (now - app.start_time).total_seconds()
                mins = int(diff / 60)
                if mins == 0:
                    return "Meeting now", 0
                elif mins == 1:
                    return '1 min late to check in', 0
                elif mins <= 5:
                    return f"{mins} mins late to check in", 0
                elif mins <= 10:
                    return f"{mins} mins late to check in", 1
                elif mins <= 60:
                    return f"{mins} mins late to check in", 2
                else:
                    hours = int(mins/60)
                    if hours == 1:
                        return "1 hour late to check in", 2
                    else:
                        return f"{hours} hours late to check in", 2
            
            # if not in meeting or late to one, then just show the start time of next meeting
            next_appointment = appointments.exclude(checked_in=True).order_by('start_time').first()
            if next_appointment is None:
                return "No upcoming appointments", 0
            return f"Next appointment in {next_appointment.time_from_now()}", 0
        except:
            return ""


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
    check_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.therapist.name} - {self.client.name} - {self.start_time}"

    def time_from_now(self):
        try:
            now = timezone.now()
            diff = self.start_time - now
            end_diff = self.end_time - now
            num_seconds = diff.total_seconds()
            end_seconds = end_diff.total_seconds()
            if (end_seconds > 0) and (num_seconds <= 0):
                return "In progress"
            if num_seconds >= 0:
                if num_seconds >= 3600:
                    return f"{int(num_seconds/3600)} hours from now"
                return f"{int(num_seconds/60)} mins from now"
            else:
                if num_seconds <= 3600:
                    hours = int(-1*num_seconds/3600 + 0.5)
                    if hours == 1:
                        return f"{hours} hour ago"    
                    if hours > 1:
                        return f"{hours} hours ago"    
                return f"{int(-1*num_seconds/60)} mins ago"
        except:
            return ""