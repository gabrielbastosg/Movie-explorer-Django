from django.shortcuts import render,redirect
import requests
from decouple import config
from .models import FavoriteMovie
from django.contrib import messages
from django.contrib.auth.decorators import login_required

API_KEY = config("TMDB_API_KEY")

# Create your views here.
def home(request):
    query = request.GET.get("q")
    genre_id = request.GET.get("genre")
    page = request.GET.get("page", 1)

    # Buscar lista de gêneros
    genres_url = (
        f"https://api.themoviedb.org/3/genre/movie/list"
        f"?api_key={API_KEY}&language=pt-BR"
    )
    genres_response = requests.get(genres_url)
    genres = genres_response.json()["genres"]

    # Escolher qual busca fazer
    if query:
        url = (
            f"https://api.themoviedb.org/3/search/movie"
            f"?api_key={API_KEY}&language=pt-BR&query={query}&page={page}"
        )
    else:
        url = (
            f"https://api.themoviedb.org/3/discover/movie"
            f"?api_key={API_KEY}&language=pt-BR&page={page}&sort_by=popularity.desc"
        )

# Se gênero foi selecionado, adiciona filtro
    if genre_id:
        url += f"&with_genres={genre_id}"

    response = requests.get(url)
    data = response.json()
    movies = data["results"]
    total_pages = data["total_pages"]

    return render(request, "movies/home.html", {
        "movies": movies,
        "query": query,
        "genres": genres,
        "selected_genre": genre_id,
        "page": int(page),
        "total_pages": total_pages,
    })

def movie_detail(request,movie_id):
    url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}"
        f"?api_key={API_KEY}&language=pt-BR"
    )

    response = requests.get(url)
    movie = response.json()

    #Buscar videos/trailers dos filmes
    video_url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}/videos"
        f"?api_key={API_KEY}&language=pt-BR"
    ) 
    video_response = requests.get(video_url)
    videos = video_response.json()["results"]

    trailer_key = None

    #Procurar trailer do youtube
    for video in videos:
        if (
            video["site"] == "YouTube"
            and video["type"] == "Trailer"
            and video.get("official", False)
        ):
            trailer_key = video["key"]
            break
    # Se não achar trailer oficial, pega qualquer vídeo do YouTube
    if not trailer_key:
        for video in videos:
            if video["site"] == "YouTube":
                trailer_key = video["key"]
                break

    is_favorite = FavoriteMovie.objects.filter(movie_id=movie_id).exists()

    return render(request,"movies/movie_detail.html",{
        "movie":movie,
        "trailer_key": trailer_key,
        "movie_id":movie_id,
        "is_favorite":is_favorite
    })

@login_required
def add_favorite(request,movie_id):
    url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}"
        f"?api_key={API_KEY}&language=pt-BR"
    )

    response = requests.get(url)
    movie = response.json()

    FavoriteMovie.objects.get_or_create(
        movie_id=movie["id"],
        title=movie["title"],
        poster_path=movie["poster_path"],
    )

    messages.success(request, "✅ Filme adicionado aos favoritos!")

    return redirect("movie_detail", movie_id=movie_id)

@login_required
def favorites(request):
    favorites = FavoriteMovie.objects.all()

    return render(request,"movies/favorites.html",{
        "favorites":favorites
    })


@login_required
def remove_favorite(request, movie_id):
    FavoriteMovie.objects.filter(movie_id=movie_id).delete()
   
    messages.success(request, "❌ Filme removido dos favoritos!")
    
    return redirect("favorites")
