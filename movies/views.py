from django.shortcuts import render
import requests
from decouple import config
API_KEY = config("TMDB_API_KEY")

# Create your views here.
def home(request):
    query = request.GET.get("q")
    genre_id = request.GET.get("genre")

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
            f"?api_key={API_KEY}&language=pt-BR&query={query}"
        )
    else:
        url = (
            f"https://api.themoviedb.org/3/discover/movie"
            f"?api_key={API_KEY}&language=pt-BR"
        )

# Se gênero foi selecionado, adiciona filtro
    if genre_id:
        url += f"&with_genres={genre_id}"

    response = requests.get(url)
    data = response.json()
    movies = data["results"]

    return render(request, "movies/home.html", {
        "movies": movies,
        "query": query,
        "genres": genres,
        "selected_genre": genre_id,
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


    return render(request,"movies/movie_detail.html",{
        "movie":movie,
        "trailer_key": trailer_key,
    })


