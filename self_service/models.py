# models.py
from django.db import models
from django.contrib.auth.models import User

class ExcelData(models.Model):
    process_id = models.CharField(max_length=255)
    cg_pno = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    rank = models.CharField(max_length=255)
    unit_descriptions = models.CharField(max_length=255)
    batch = models.CharField(max_length=255)
    uploaded_on = models.DateField(null=True)  # Allow NULL values
    user_name = models.CharField(max_length=255)
    process_name = models.CharField(max_length=255)
    form_no = models.CharField(max_length=255)
    refrence_type = models.CharField(max_length=255)
    form_type = models.CharField(max_length=255)
    from_date = models.DateField(null=True)
    allocated_on = models.DateField(null=True)
    task_to = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    stage = models.CharField(max_length=255)
    approver_remarks = models.TextField()
    verifier_remarks = models.TextField()
    initiator_remarks = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)  # Automatically set to the current date and time

    def __str__(self):
        return f"{self.process_id} - {self.user_name} - {self.update_date} - {self.upload_date}"

class Notification(models.Model):
    heading = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading

class UserQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pf_no = models.CharField(max_length=200)
    pf_unit = models.CharField(max_length=100)
    description = models.TextField()
    admin_reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Automatically link to the User model
    subject = models.CharField(max_length=100, blank=False, null=False)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} on {self.created_at}"
