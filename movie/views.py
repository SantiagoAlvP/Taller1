# Username: admin
# Email: admin@admin.com
# Password: admin
#///////////////////////////////////////////////


import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

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

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})

def statistics_view(request):
    matplotlib.use('Agg')
    
    # Gráfica de películas por año
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count
    
    bar_positions_year = range(len(movie_counts_by_year))
    
    fig, axes = plt.subplots(2, 1, figsize=(10, 10))
    
    axes[0].bar(bar_positions_year, movie_counts_by_year.values(), align='center')
    axes[0].set_title('Movies per year')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Number of movies')
    axes[0].set_xticks(bar_positions_year)
    axes[0].set_xticklabels(movie_counts_by_year.keys(), rotation=90)
    axes[0].tick_params(axis='x', which='both', bottom=False, top=False)
    
    # Gráfica de películas por género
    genres = Movie.objects.values_list('genre', flat=True).distinct().order_by('genre')
    movie_counts_by_genre = {}
    for genre in genres:
        if genre:
            movies_in_genre = Movie.objects.filter(genre=genre)
        else:
            movies_in_genre = Movie.objects.filter(genre__isnull=True)
            genre = "None"
        count = movies_in_genre.count()
        movie_counts_by_genre[genre] = count
    
    bar_positions_genre = range(len(movie_counts_by_genre))
    
    axes[1].bar(bar_positions_genre, movie_counts_by_genre.values(), align='center')
    axes[1].set_title('Movies per genre')
    axes[1].set_xlabel('Genre')
    axes[1].set_ylabel('Number of movies')
    axes[1].set_xticks(bar_positions_genre)
    axes[1].set_xticklabels(movie_counts_by_genre.keys(), rotation=90)
    axes[1].tick_params(axis='x', which='both', bottom=False, top=False)
    
    # Guardar la gráfica como imagen
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    return render(request, 'statistics.html', {'graphic': graphic})
