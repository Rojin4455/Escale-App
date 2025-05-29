from decouple import config
import requests
from django.http import JsonResponse
import json
from django.shortcuts import redirect, render
from accounts.models import GHLAuthCredentials
from django.views.decorators.csrf import csrf_exempt
from accounts.helpers import get_location_data
# Create your views here.
from accounts.models import WebhookLog
from accounts.tasks import handle_webhook_event


GHL_CLIENT_ID = config("GHL_CLIENT_ID")
GHL_CLIENT_SECRET = config("GHL_CLIENT_SECRET")
GHL_REDIRECTED_URI = config("GHL_REDIRECTED_URI")
TOKEN_URL = "https://services.leadconnectorhq.com/oauth/token"
SCOPE = config("SCOPE")


def onboard(request):
    return render(request,'onboard.html')


def auth_connect(request):
    auth_url = ("https://marketplace.leadconnectorhq.com/oauth/chooselocation?response_type=code&"
                f"redirect_uri={GHL_REDIRECTED_URI}&"
                f"client_id={GHL_CLIENT_ID}&"
                f"scope={SCOPE}"
                )
    return redirect(auth_url)



def callback(request):
    
    code = request.GET.get('code')

    if not code:
        return JsonResponse({"error": "Authorization code not received from OAuth"}, status=400)

    return redirect(f'{config("BASE_URI")}/auth/tokens?code={code}')


def tokens(request):
    authorization_code = request.GET.get("code")

    if not authorization_code:
        return JsonResponse({"error": "Authorization code not found"}, status=400)

    data = {
        "grant_type": "authorization_code",
        "client_id": GHL_CLIENT_ID,
        "client_secret": GHL_CLIENT_SECRET,
        "redirect_uri": GHL_REDIRECTED_URI,
        "code": authorization_code,
    }

    response = requests.post(TOKEN_URL, data=data)

    try:
        response_data = response.json()
        if not response_data:
            return


        location_data = get_location_data(location_id=response_data.get("locationId"), access_token=response_data.get("access_token"))
        if location_data:
            
            # print("location Data: ", location_data)
            response_data["location_name"] = location_data['location']['name']
            if not response_data.get('access_token'):
                return render(request, 'onboard.html', context={
                    "message": "Invalid JSON response from API",
                    "status_code": response.status_code,
                    "response_text": response.text[:400]
                }, status=400)

            obj, created = GHLAuthCredentials.objects.update_or_create(
                location_id= response_data.get("locationId"),
                defaults={
                    "access_token": response_data.get("access_token"),
                    "refresh_token": response_data.get("refresh_token"),
                    "expires_in": response_data.get("expires_in"),
                    "scope": response_data.get("scope"),
                    "user_type": response_data.get("userType"),
                    "company_id": response_data.get("companyId"),
                    "user_id":response_data.get("userId"),
                    "location_name":response_data.get("location_name")

                }
            )
            return render(request, 'onboard.html', context = {
                "message": "Authentication successful",
                "access_token": response_data.get('access_token'),
                "token_stored": True
            })
        
    except requests.exceptions.JSONDecodeError:
        return render(request, 'onboard.html', context={
            "error": "Invalid JSON response from API",
            "status_code": response.status_code,
            "response_text": response.text[:500]
        }, status=500)
    

# print("swws",GHLAuthCredentials.objects.first())

def get_token(request):
    location_id = request.GET.get('locationId')
    if not location_id:
        return JsonResponse({'error': 'Missing locationId in query params'}, status=400)
    try:
        token = GHLAuthCredentials.objects.get(location_id=location_id)
        return JsonResponse({'access_token': token.access_token})
    except GHLAuthCredentials.DoesNotExist:
        return JsonResponse({'error': 'Token not found for the given locationId'}, status=404)
    




@csrf_exempt
def webhook_handler_for_opportunity(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        print("date:----- ", data)
        if data["webhookId"]:
            try:
                WebhookLog.objects.get(webhook_id = data["webhookId"])
                return JsonResponse({"message":"Webhook Already Recieved"}, status=200)
            except WebhookLog.DoesNotExist:
                WebhookLog.objects.create(data=data, webhook_id=data['webhookId'])
                event_type = data.get("type")
                handle_webhook_event.delay(data, event_type)
                return JsonResponse({"message":"Webhook received"}, status=200)
    except Exception as e:
        print("error response: ", str(e))
        return JsonResponse({"error": str(e)}, status=500)
