from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from .models import UploadedImage


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
    context = {
        'username': username,
        'city': city,
        'country': country,
        'text': text
    }
    print(context)

    return JsonResponse(context)


def image_detail(request, pk):
    uploaded_image = get_object_or_404(UploadedImage, pk=pk)
    return render(request, 'image_detail.html', {'uploaded_image': uploaded_image})


def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        uploaded_image = UploadedImage.objects.create(image=image)
        return redirect('image_detail', pk=uploaded_image.pk)
    return render(request, 'upload.html')
