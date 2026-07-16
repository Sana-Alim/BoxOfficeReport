import requests
import os

MONTH = "2026-05"

response = requests.get(
    "https://prodapifree.reco-bee.com/common/v2/movies/recent"
)

movies = response.json()

filtered_movies = []

for movie in movies:

    release_date = movie.get(
        "releasedatetmdb",
        ""
    )

    if release_date.startswith(MONTH):
        filtered_movies.append(movie)

print("Movies in month:", len(filtered_movies))
os.makedirs("reports", exist_ok=True)

with open(
    "templates/report_template.html",
    "r"
) as file:

    html = file.read()

print("Template loaded")

total_releases = len(filtered_movies)

total_gross = total_releases * 100

average_gross = total_gross / total_releases

top_film = filtered_movies[0]["title"]

highest_gross_film = filtered_movies[0]["title"]
highest_gross = 100

best_opening_film = filtered_movies[0]["title"]
best_opening = 20


movie_cards = ""

for movie in filtered_movies:

    movie_cards += f"""
    <div class="movie-card">

        <img src="{movie.get('posterimageurl')}" alt="{movie.get('title')}">

        <div class="movie-info">
            <div class="movie-title">{movie.get('title')}</div>

            <p><strong>Language:</strong> {', '.join(movie.get('language', []))}</p>

            <p><strong>Release Date:</strong> {movie.get('releasedatetmdb')}</p>

        </div>

        <div class="stat-box">
            <div class="stat-icon">⊙</div>
            <div class="stat-value">₹100 Cr</div>
            <div class="stat-label">Gross (Cr)</div>
        </div>

        <div class="stat-box">
            <div class="stat-icon">🎟</div>
            <div class="stat-value">₹20 Cr</div>
            <div class="stat-label">Opening Weekend</div>
        </div>

    </div>
    """


html = html.replace(
    "{{TOTAL_RELEASES}}",
    str(total_releases)
)

html = html.replace(
    "{{TOTAL_GROSS}}",
    str(total_gross)
)

html = html.replace(
    "{{AVERAGE_GROSS}}",
    str(int(average_gross))
)

html = html.replace(
    "{{TOP_FILM}}",
    top_film
)

html = html.replace(
    "{{HIGHEST_GROSS_FILM}}",
    highest_gross_film
)

html = html.replace(
    "{{HIGHEST_GROSS}}",
    str(highest_gross)
)

html = html.replace(
    "{{BEST_OPENING_FILM}}",
    best_opening_film
)

html = html.replace(
    "{{BEST_OPENING}}",
    str(best_opening)
)

html = html.replace(
    "{{MOVIE_CARDS}}",
    movie_cards
)

report_path = "reports/report-may-2026.html"

with open(report_path, "w") as file:
    file.write(html)

print("Report created:", report_path)
