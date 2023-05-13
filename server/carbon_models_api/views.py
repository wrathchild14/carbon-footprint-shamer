from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import CarbonData


def process_text(request, username, city, country, text):
    context = {
        'username': username,
        'city': city,
        'country': country,
        'text': text
    }
    print(context)

    return JsonResponse(context)


def save_data(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        # damages = request.POST.get('damages')
        damages = 69
        # carbon = request.POST.get('carbon')
        carbon = 25
        image_path = request.FILES.get('image_path')

        carbon_data = CarbonData(name=name , damages=damages, carbon=carbon, image_path=image_path)
        carbon_data.save()
        return redirect('list_data')

    return render(request, 'data_form.html')


def list_data(request):
    carbon_data = CarbonData.objects.all()
    return render(request, 'data_list.html', {'carbon_data': carbon_data})
