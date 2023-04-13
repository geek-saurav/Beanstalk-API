# Django imports
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password

# DRF imports
from rest_framework.decorators import api_view

# python imports
import json

# email validator
from email_validator import validate_email, EmailNotValidError

# Model import
from api.models import User

# Helpers
from api.helpers import get_tokens

# exceptions


@api_view(["POST"])
def signup(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data['email']
    name = data['name']
    password = data['password']
    confirm_password = data['confirm_password']

    try:
        email_validator = validate_email(email, check_deliverability=True)
        email = email_validator.email
    except EmailNotValidError as e:
        return JsonResponse({'error': "Email address or domain is not valid !"}, status=400)
    
    if password != confirm_password:
        return JsonResponse({"error": "Passwords do not match!"}, status=400)
    else:
        try:
            user = User(
                name=name,
                username=email,
                email=email,
                password=make_password(password)
            )
            user.save()
            user_details = user.to_dict()
            tokens = get_tokens(user)

            return JsonResponse({**user_details, **tokens}, status=200)
        except Exception as e:
            exception_class = f"{e.__class__.__name__}"
            if exception_class == "IntegrityError":
                return JsonResponse({"error": "User already exists!"}, status=400)
        
@api_view(["POST"])
def login(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data['email']
    password = data['password']

    if not (email and password):
        return JsonResponse({"error": "Incomplete credentials provided"}, status=400)
    
    try:
        user=User.objects.get(email=email)

        if check_password(password, user.password):
            user_details = user.to_dict()
            tokens = get_tokens(user)

            return JsonResponse({**user_details, **tokens}, status=200)
        else:
            return JsonResponse({"error": "Password does not match!"}, status=400)
    except Exception as e:
        exception_class = f"{e.__class__.__name__}"
        
        if exception_class == "DoesNotExist":
            return JsonResponse({"error": "User does not exist!"}, status=400)