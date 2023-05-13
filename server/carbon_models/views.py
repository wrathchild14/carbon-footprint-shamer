from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
# import joblib
import json


def predict(request):
    if request.method == 'POST':
        # Load the ML model
        # prediction = model.predict([[feature1, feature2]])
        prediction = ""
        # Return the prediction as JSON
        response = {'prediction': prediction}
        return JsonResponse(response)

    return JsonResponse({'error': 'Invalid request method'})


def process_text(request, username, city, country, text):
    # Perform any processing or operations with the received data

    context = {
        'username': username,
        'city': city,
        'country': country,
        'text': text
    }
    print(context)

    return JsonResponse(context)
