

import pandas as pd
from accounts.models import Opportunity  # Update this with your actual app name
from django.utils.dateparse import parse_datetime
from accounts.models import GHLAuthCredentials

def import_and_create_oppor(file, locationId):
    location = GHLAuthCredentials.objects.get(location_id = locationId)


    # Load the Excel file
    file_path = file  # Change this to your actual file path
    df = pd.read_excel(file_path, engine="openpyxl")
    print(len(df))
    return
    # df = pd.read_excel(file_path, sheet_name="Accounts Opportunity", dtype=str)


    # Mapping column names from the sheet to Django model fields
    column_mapping = {
        "Opportunity Name": "opportunity_name",
        "Contact Name": "full_name",
        "phone": "phone",
        "email": "email",
        "pipeline": "pipeline_name",
        "stage": "pipeline_stage",
        "Lead Value": "lead_value",
        "source": "source",
        "assigned": "assigned",
        "Created on": "date_created",
        "Updated on": "updated_on",
        "lost reason ID": "lost_reason_id",
        "lost reason name": "lost_reason_name",
        "Followers": "followers",
        "Notes": "notes",
        "tags": "tags",
        "Engagement Score": "engagement_score",
        "status": "status",
        "Booked By": "booked_by",
        "Opportunity ID": "opportunity_id",
        "Contact ID": "contact_id",
        "Pipeline Stage ID": "pipeline_stage_id",
        "Pipeline ID": "pipeline_id",
        "Days Since Last Stage Change Date ": "days_since_last_stage_change",
        "Days Since Last Status Change Date ": "days_since_last_status_change",
        "Days Since Last Updated ": "days_since_last_updated",
    }

    # Rename DataFrame columns
    df = df.rename(columns=column_mapping)

    # Fill empty values with "No Data" except for numeric fields
    for col in df.columns:
        if df[col].dtype == object:  # Only apply to string fields
            df[col] = df[col].fillna("No Data")
        else:
            df[col] = df[col].fillna(0)  # Fill numeric fields with 0

    # Convert date fields
    # date_fields = ["date_created", "updated_on"]
    # for field in date_fields:
    #     df[field] = df[field].apply(lambda x: parse_datetime(str(x)) if pd.notnull(x) else None)

    # Iterate over DataFrame and update or create records
    new_opportunities = []
    for _, row in df.iterrows():
        opportunity_id = row["opportunity_id"]
        if opportunity_id and opportunity_id != "No Data":  # Ensure ID is valid
            # new_opportunities.append(Opportunity(**row.to_dict()))
            row_dict = row.to_dict()
            row_dict["location_id"] = location.location_id
            row_dict["location_name"] = location.location_name
            new_opportunities.append(Opportunity(**row_dict))

            # obj, created = Opportunity.objects.update_or_create(
            #     opportunity_id=opportunity_id,  # Lookup field
            #     defaults=row.to_dict(),  # Update/Create with row data
            # )

    if new_opportunities:
        Opportunity.objects.bulk_create(new_opportunities)
        print(f"Inserted {len(new_opportunities)} new opportunities.")
    else:
        print("No new opportunities to insert.")

    print("Data import complete.")