# Django imports
from django.http import HttpResponse, JsonResponse
from beanstalkDjango.settings import OPENAI_KEY

# DRF imports
from rest_framework.decorators import api_view

# openai imports
import openai

# python default imports
import json


# openai key init
openai.api_key = OPENAI_KEY
# Create your views here.
@api_view(['GET'])
def test(request):
    return HttpResponse('Hello world!', status=200)

@api_view(['POST'])
def generate_api(request):
    data = json.loads(request.body.decode('utf-8'))
    model_name = data['model_name']
    backend = data['backend']
    framework = data['framework']
    language = data['language']
    prompt = f"For a {model_name} database model , generate {backend} db connection for {framework}, {framework} database model, {framework} CRUD endpoints code. Appropriately comment each section"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = [{
            "role": "user",
            "content": prompt
            }],
            temperature=0.7,
            max_tokens=2000
        )
        
        
        api_code = response["choices"][0]["message"]["content"]
        api_code = api_code.replace('"', '')
        res_dict = {}

        lang = language

        res_dict['language'] = lang.lower()
        res_dict['code'] = api_code
        return JsonResponse(res_dict, status=200)
    except Exception as e:
        return HttpResponse(f"Something went wrong with exception {e}", status=400)