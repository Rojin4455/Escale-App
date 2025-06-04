# your_app_name/tasks.py
import requests
from celery import shared_task
from accounts.models import GHLAuthCredentials, Opportunity, CustomField
from decouple import config
from accounts.helpers import get_ghl_opportunity,create_opportunity, update_opportunity, get_custom_field

@shared_task(name="accounts.tasks.make_api_call")
def make_api_call():
    tokens = GHLAuthCredentials.objects.all()

    for credentials in tokens:
    
        print("credentials tokenL", credentials)
        refresh_token = credentials.refresh_token

        
        response = requests.post('https://services.leadconnectorhq.com/oauth/token', data={
            'grant_type': 'refresh_token',
            'client_id': config("GHL_CLIENT_ID"),
            'client_secret': config("GHL_CLIENT_SECRET"),
            'refresh_token': refresh_token
        })
        
        new_tokens = response.json()
        print("responseL ", new_tokens)
        obj, created = GHLAuthCredentials.objects.update_or_create(
                location_id= new_tokens.get("locationId"),
                defaults={
                    "access_token": new_tokens.get("access_token"),
                    "refresh_token": new_tokens.get("refresh_token"),
                    "expires_in": new_tokens.get("expires_in"),
                    "scope": new_tokens.get("scope"),
                    "user_type": new_tokens.get("userType"),
                    "company_id": new_tokens.get("companyId"),
                    "user_id":new_tokens.get("userId"),

                }
            )



@shared_task
def handle_webhook_event(data, event_type):
    print("webhook Data: ", data)
    location = GHLAuthCredentials.objects.get(location_id = data['locationId'])
    if event_type == "OpportunityDelete":
        
        opportunity_id = data.get("id")
        if opportunity_id:
            opportunity = Opportunity.objects.filter(opportunity_id=opportunity_id).first()
            if opportunity:
                opportunity.delete()
                print("Opportunity is deleted")
            else:
                print("Opportunity not found")
    else:

        opportunity_data = get_ghl_opportunity(data.get("id"), location.access_token)
        if opportunity_data.get("error"):
            return

        
        opportunity = opportunity_data.get("opportunity")       

        if "customFields" in opportunity:
            for field in opportunity["customFields"]:
                field_id = field.get("id")
                field_value = field.get("fieldValue")

                try:
                    # Check if custom field exists in the DB
                    custom_exists = CustomField.objects.get(field_id=field_id)
                    if custom_exists.field_name == "Booked By":
                        opportunity["Booked By"] = field_value
                        break
                except CustomField.DoesNotExist:
                    print("not exists")
                    # Fetch custom field details from external API
                    custom_field_response = get_custom_field(
                        id=field_id,
                        access_token=location.access_token,
                        location_id=location.location_id
                    )

                    custom_field = custom_field_response.get("customField")
                    if custom_field and custom_field.get("name") == "Booked By":
                        # Save to DB
                        CustomField.objects.create(
                            field_name=custom_field["name"],
                            location_id=location.location_id,
                            field_id=field_id
                        )
                        opportunity["Booked By"] = field_value
                        break

        if "Booked By" not in opportunity:
            opportunity["Booked By"] = ""

        if not opportunity.get("Booked By"):
            opportunity["Booked By"] = ""
        if event_type in ["OpportunityCreate"]:
            if opportunity:
                create_opportunity(opportunity, location)

        if event_type == "OpportunityUpdate":
            
            
            if opportunity:
                update_opportunity(opportunity, location)



            else:
                print("Opportunity ID missing in data")