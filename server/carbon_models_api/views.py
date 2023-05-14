import os

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
        country = request.POST.get('country')
        message = request.POST.get('message')
        if not message:
            message = "No message attached"
            image_path = request.FILES.get('image_path')

            from carbon_models_api.model_controllers.ds import FootPrintImage
            print_image = FootPrintImage("", "")
            carbon, lista = print_image.image_process(os.getcwd() + "/carbon_models_api/examples/" + str(image_path),
                                                      str(country))

        else:
            from carbon_models_api.model_controllers.ds import FootPrintText
            text_model = FootPrintText("", "")
            carbon, lista = text_model.text_footprint(message, str(country))

            image_path = os.path.join(os.getcwd(), 'media', 'logo.png')

        damages = ' '.join(lista)
        carbon_data = CarbonData(name=name, message=message, carbon=carbon, damages=damages, image_path=image_path,
                                 country=country)

        carbon_data.save()
        return redirect('list_data')

    return render(request, 'data_form.html')


def list_data(request):
    carbon_data = CarbonData.objects.all()
    reversed_data = list(carbon_data)[::-1]

    sorted_by_carbon = CarbonData.objects.order_by('carbon')

    return render(request, 'data_list.html',
                  {'carbon_data': reversed_data, 'sorted_by_carbon': list(sorted_by_carbon)[::-1]})
