from django.shortcuts import get_object_or_404, redirect, render
import requests 
from decouple import config
from pprint import pprint
from .models import City
from django.contrib import messages

# Create your views here.
def home(request):
    cities = City.objects.all()
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
    # city = 'Istanbul'

    # a = {
    #     'a': 'javid'
    # }
    # print(a.get('a'))

    g_city = request.GET.get('city')
    print('g_city:', g_city)
    if g_city:
        response = requests.get(url.format(g_city, config('API_KEY')))
        print(response.status_code)
        if response.status_code == 200:
            content = response.json()
            a_city = content['name']
            if City.objects.filter(name=a_city):
                messages.warning(request, 'City already exists')
            else:
                City.objects.create(name=a_city)
                messages.success(request, 'City successfully created')
        else:
            messages.warning(request, 'City does not exists')
        return redirect('home')

      

    city_data = []
    for city in cities: 
        print(city)
        response = requests.get(url.format(city, config('API_KEY'))).json()


    # pprint(response)

        data = {
            'city': city,
            'temp': response['main']['temp'],
            'desc': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon']
        }
        city_data.append(data)
    # print(city_data)
    context = {
        'city_data': city_data
    }

    return render(request, 'weather_app/home.html', context)

def delete_city(request, id):
    city = get_object_or_404(City, id=id)
    city.delete()
    return redirect('home')