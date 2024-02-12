# Username: admin
# Email: admin@admin.com
# Password: admin
#///////////////////////////////////////////////

from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

# Create your views here.

def home(request):
    """ return HttpResponse('<h1>Welcome to Home Page</h1>')
     return render(request, 'home.html')
     return render(request, 'home.html', {'name':'Santiago Alvarez'})"""
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:        
        movies = Movie.objects.all()
    return render(request, 'home.html', {'movies':movies, 'searchTerm':searchTerm})
    

def about(request):
    # return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'about.html')

