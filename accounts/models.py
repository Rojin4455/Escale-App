from django.db import models

class GHLAuthCredentials(models.Model):
    user_id = models.CharField(max_length=255, null=True, blank=True)
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_in = models.IntegerField()
    scope = models.TextField(null=True, blank=True)
    user_type = models.CharField(max_length=50, null=True, blank=True)
    company_id = models.CharField(max_length=255, null=True, blank=True)
    location_id = models.CharField(max_length=255, null=True, blank=True)
    location_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user_id} - {self.company_id} - {self.location_id}"
    
class WebhookLog(models.Model):
    received_at = models.DateTimeField(auto_now_add=True)
    data = models.TextField(null=True, blank=True)
    webhook_id = models.CharField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.webhook_id} : {self.received_at}"
    

class CustomField(models.Model):
    location_id = models.CharField(max_length=255, null=True, blank=True)
    field_name = models.CharField(max_length=255, null=True, blank=True)
    field_id = models.CharField(max_length=255, null=True, blank=True)

class Opportunity(models.Model):
    contact_id = models.CharField(max_length=255, null=True, blank=True)
    location_id = models.CharField(max_length=255, null=True, blank=True)
    location_name = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.CharField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    opportunity_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    pipeline_name = models.CharField(max_length=255, null=True, blank=True)
    pipeline_stage = models.CharField(max_length=255, null=True, blank=True)
    lead_value = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    assigned = models.CharField(max_length=255, null=True, blank=True, default="No Data")
    updated_on = models.CharField(null=True, blank=True)
    lost_reason_id = models.CharField(max_length=255, null=True, blank=True,default="No Data")
    lost_reason_name = models.CharField(max_length=255, default="No Data")
    followers = models.TextField(default="No Data")
    notes = models.TextField(default="No Data")
    tags = models.CharField(max_length=255, null=True, blank=True)
    engagement_score = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    booked_by = models.CharField(max_length=255, null=True, blank=True)
    opportunity_id = models.CharField(max_length=255, null=True, blank=True)
    pipeline_stage_id = models.CharField(max_length=255, null=True, blank=True)
    pipeline_id = models.CharField(max_length=255, null=True, blank=True)
    days_since_last_stage_change = models.CharField(max_length=50, null=True, blank=True)
    days_since_last_status_change = models.CharField(max_length=50, null=True, blank=True)
    days_since_last_updated = models.CharField(max_length=50, default="No Data")

    class Meta:
        db_table = 'opportunity'

    def __str__(self):
        return self.full_name or "Unnamed Opportunity"
