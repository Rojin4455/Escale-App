import requests
from accounts.models import Opportunity

def get_location_data(location_id, access_token):
    url = f"https://services.leadconnectorhq.com/locations/{location_id}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Version": "2021-07-28"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("response location: ", response.json())
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
    

def get_ghl_opportunity(oppertunity_id, access_token):
    url = f"https://services.leadconnectorhq.com/opportunities/{oppertunity_id}"
    
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Version": "2021-07-28"
    }
    
    response = requests.get(url, headers=headers)

    print("response: ", response.json())
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}



def create_opportunity(opportunity_data, location):

    source = opportunity_data.get("source")
    source = source.get("source", "No Data") if isinstance(source, dict) else (source or "No Data")
    opp_id = opportunity_data["id"]
    contact_id = opportunity_data["contactId"]
    full_name = opportunity_data.get("contact", {}).get("name", "No Data")
    email = opportunity_data.get("contact", {}).get("email", "No Data")
    phone = opportunity_data.get("contact", {}).get("phone", "No Data")
    tags = ", ".join(opportunity_data.get("contact", {}).get("tags", []))
    date_created = opportunity_data.get("createdAt")
    updated_on = opportunity_data.get("updatedAt")
    status = opportunity_data.get("status")
    lead_value = opportunity_data.get("monetaryValue")
    pipeline_stage_id = opportunity_data.get("pipelineStageId", "No Data")
    pipeline_id = opportunity_data.get("pipelineId", "No Data")
    assigned = opportunity_data.get("assignedTo", "No Data")
    opportunity_name = opportunity_data.get("name", "No Data")
    days_since_last_stage_change = opportunity_data.get("lastStageChangeAt")
    days_since_last_status_change = opportunity_data.get("lastStatusChangeAt")

    # Look up pipeline stage name
    pipeline_stage_name = "Unknown Stage"

    # for stage in get_pipeline_stages()["stages"]:
    #     if stage["id"] == pipeline_stage_id:
    #         pipeline_stage_name = stage["name"]
    #         break

    def get_pipeline_and_stage_name(pipeline_stage_id):
        response = get_pipelines(location_id=location.location_id, access_token=location.access_token)  # This should return the JSON structure you posted
        for pipeline in response.get("pipelines", []):
            for stage in pipeline.get("stages", []):
                if stage["id"] == pipeline_stage_id:
                    return pipeline["name"], stage["name"]
        return None, None

# Get the pipeline and stage names dynamically
    pipeline_name, pipeline_stage_name = get_pipeline_and_stage_name(pipeline_stage_id)

    # Create or update the opportunity in the database
    opportunity_obj = Opportunity.objects.create(
        opportunity_id=opp_id,
        contact_id=contact_id,
        full_name=full_name,
        email=email,
        phone=phone,
        tags=tags,
        date_created=date_created,
        pipeline_stage=pipeline_stage_name,
        pipeline_id=pipeline_id,
        pipeline_name=pipeline_name,
        status=status,
        lead_value=lead_value,
        source=source,
        assigned=assigned,
        opportunity_name=opportunity_name,
        days_since_last_stage_change=days_since_last_stage_change,
        days_since_last_status_change=days_since_last_status_change,
        updated_on=updated_on,
        pipeline_stage_id=pipeline_stage_id,
        booked_by=opportunity_data["Booked By"]
    )

    print("Oppeortunity created successfully")

    return opportunity_obj



def update_opportunity(opportunity_data, location):
    print("opportunity Data: ", opportunity_data)
    source = opportunity_data.get("source")
    source = source.get("source", "No Data") if isinstance(source, dict) else (source or "No Data")
    opp_id = opportunity_data["id"]
    contact_id = opportunity_data["contactId"]
    full_name = opportunity_data.get("contact", {}).get("name", "No Data")
    email = opportunity_data.get("contact", {}).get("email", "No Data")
    phone = opportunity_data.get("contact", {}).get("phone", "No Data")
    tags = ", ".join(opportunity_data.get("contact", {}).get("tags", []))
    date_created = opportunity_data.get("createdAt")
    updated_on = opportunity_data.get("updatedAt")
    status = opportunity_data.get("status")
    lead_value = opportunity_data.get("monetaryValue")
    pipeline_stage_id = opportunity_data.get("pipelineStageId", "No Data")
    pipeline_id = opportunity_data.get("pipelineId", "No Data")
    assigned = opportunity_data.get("assignedTo", "No Data")
    opportunity_name = opportunity_data.get("name", "No Data")
    days_since_last_stage_change = opportunity_data.get("lastStageChangeAt")
    days_since_last_status_change = opportunity_data.get("lastStatusChangeAt")

    # Look up pipeline stage name
    pipeline_stage_name = "Unknown Stage"



    def get_pipeline_and_stage_name(pipeline_stage_id):
        response = get_pipelines(location_id=location.location_id, access_token=location.access_token)
        for pipeline in response.get("pipelines", []):
            for stage in pipeline.get("stages", []):
                if stage["id"] == pipeline_stage_id:
                    return pipeline["name"], stage["name"]
        return None, None

    pipeline_name, pipeline_stage_name = get_pipeline_and_stage_name(pipeline_stage_id)


    opportunity_obj, created = Opportunity.objects.update_or_create(
    opportunity_id=opp_id,
    defaults={
        "contact_id": contact_id,
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "tags": tags,
        "date_created": date_created,
        "pipeline_stage": pipeline_stage_name,
        "pipeline_id": pipeline_id,
        "pipeline_name": pipeline_name,
        "status": status,
        "lead_value": lead_value,
        "source": source,
        "assigned": assigned,
        "opportunity_name": opportunity_name,
        "days_since_last_stage_change": days_since_last_stage_change,
        "days_since_last_status_change": days_since_last_status_change,
        "updated_on": updated_on,
        "pipeline_stage_id": pipeline_stage_id,
        "location_id": location.location_id,
        "location_name": location.location_name,
        "booked_by":opportunity_data["Booked By"]
    }
)

    if created:
        print("opportunity created in update method")
    else:
        print("Opportunity udated successfully")

    return opportunity_obj



def get_pipelines(location_id: str, access_token: str):
    url = f"https://services.leadconnectorhq.com/opportunities/pipelines?locationId={location_id}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Version": "2021-07-28"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise error for HTTP 4xx/5xx responses
        return response.json()       # Return parsed JSON response
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response: {response.text}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None



def get_custom_field(id: str, location_id: str, access_token: str):
    url = f"https://services.leadconnectorhq.com/locations/{location_id}/customFields/{id}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Version": "2021-07-28"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response: {response.text}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None