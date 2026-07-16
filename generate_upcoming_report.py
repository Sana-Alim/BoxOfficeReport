import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

today = datetime.now()

next_month = today + relativedelta(months=1)

selected_month = next_month.month
selected_year = next_month.year
month_name = calendar.month_name[selected_month]

MONTH = f"{selected_year}-{selected_month:02d}"
print("Generating report for:", MONTH)


response = requests.get(
    "https://prodapifree.reco-bee.com/common/v2/movies/upcoming"
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
print(filtered_movies[0])
with open(
    "templates/upcoming_report_template.html",
    "r"
) as file:

    html = file.read()

print("Template loaded")
movie_cards = ""

for movie in filtered_movies:

    movie_cards = ""

for movie in filtered_movies:

    movie_cards += f"""
    <div class="movie-card">
        
        <img src="{movie.get('posterimageurl', '')}" alt="{movie.get('title', '')}">

        <div class="movie-info">

            <div class="movie-title">
                {movie.get('title', '')}
            </div>

            <p>
                <strong>Language:</strong>
                {', '.join(movie.get('language', []))}
            </p>

            <p>
    <strong>Release Date:</strong>
    <span class="date-pill">
        {movie.get('releasedatetmdb', '')}
    </span>
</p>
            <p>
                <strong>Lead Cast:</strong>
                {', '.join(movie.get('moviecast', [])[:3])}
            </p>

            <p>
    <strong>Genre:</strong>
    {"".join([f'<span class="genre-chip">{g}</span>' for g in movie.get("genre", [])])}
</p>

            <p>
    <strong>Anticipation Level:</strong>
    <span class="anticipation high">
        High
    </span>
</p>

        </div>

    </div>
    """

html = html.replace(
    "{{MOVIE_CARDS}}",
    movie_cards
)

print("Movies:", len(filtered_movies))
print("Cards:", movie_cards.count('movie-card'))
total_releases = len(filtered_movies)

html = html.replace(
    "{{TOTAL_RELEASES}}",
    str(total_releases)
)

html = html.replace(
    "{{MONTH}}",
    f"{month_name} {selected_year}"
)

report_path = (
    f"reports/upcoming-"
    f"{month_name[:3].upper()}-"
    f"{selected_year}.html"
)

with open(report_path, "w") as file:
    file.write(html)

print("Report created:", report_path)