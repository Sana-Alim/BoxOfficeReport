import requests
import random
import json

movies = requests.get(
    "https://prodapifree.reco-bee.com/common/v2/movies/recent"
).json()

report_movies = []

for movie in movies:

    release_date = movie.get("releasedatetmdb", "")

    if release_date.startswith("2026-05"):

        report_movies.append({
            "film": movie["title"],
            "language": ", ".join(movie.get("language", [])),
            "release_date": release_date,
            "gross_collection": 100,
            "opening_weekend": 20,
            "poster": movie.get("posterimageurl")
        })

report_movies.sort(
    key=lambda x: x["gross_collection"],
    reverse=True
) 

total_releases = len(report_movies)

total_gross = sum(
    movie["gross_collection"]
    for movie in report_movies
)

average_gross = round(
    total_gross / total_releases,
    1
)

highest_gross_movie = max(
    report_movies,
    key=lambda x: x["gross_collection"]
)

best_opening_movie = max(
    report_movies,
    key=lambda x: x["opening_weekend"]
)

summary = {
    "month": "May 2026",
    "total_releases": total_releases,
    "total_gross_collection": total_gross,
    "average_gross_collection": average_gross,
    "highest_grossing_film": highest_gross_movie["film"],
    "highest_gross": highest_gross_movie["gross_collection"],
    "best_opening_weekend_film": best_opening_movie["film"],
    "best_opening_weekend": best_opening_movie["opening_weekend"]
}

report = {
    "summary": summary,
    "movies": report_movies
}
with open("report.json", "w") as f:
    json.dump(report, f, indent=2)

print("report.json created successfully")

print(json.dumps(report, indent=2))