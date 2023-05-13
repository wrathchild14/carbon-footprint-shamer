from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
# import joblib
import json


def predict(request):
    if request.method == 'POST':
        # Load the ML model
        # model = joblib.load('mlmodel/models/model.pkl')
        #
        # # Get input data from the POST request
        # data = json.loads(request.body)
        # feature1 = data.get('feature1')
        # feature2 = data.get('feature2')
        #
        # # Perform prediction using the loaded model
        # prediction = model.predict([[feature1, feature2]])

        # Return the prediction as JSON
        response = {'prediction': ""}
        return JsonResponse(response)

    return JsonResponse({'error': 'Invalid request method'})
