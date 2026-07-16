import requests
from flask import Flask, request, render_template
import random

app = Flask(__name__)


def get_movies():

    url = "https://prodapifree.reco-bee.com/common/v2/movies/recent"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    print("STATUS:", response.status_code)

    if response.status_code != 200:
        return []

    return response.json()


def filter_movies_by_month(movies, month):

    filtered_movies = []

    for movie in movies:

        release_date = movie.get("releasedatetmdb", "")

        if release_date.startswith(month):
            filtered_movies.append(movie)

    return filtered_movies


@app.route("/")
def home():
    return {
        "message": "Box Office API Running"
    }


@app.route("/report")
def report():
    return render_template("report.html")


@app.route("/box-office-report")
def box_office_report():

    month = request.args.get("month")

    movies = get_movies()

    filtered_movies = filter_movies_by_month(
        movies,
        month
    )

    report_movies = []

    for movie in filtered_movies:

        report_movies.append({
            "film": movie.get("title"),
            "language": ", ".join(movie.get("language", [])),
            "release_date": movie.get("releasedatetmdb"),
            "gross_collection": 100,
            "opening_weekend": 20,
            "poster": movie.get("posterimageurl")
        })

    total_releases = len(report_movies)

    total_gross = sum(
        movie["gross_collection"]
        for movie in report_movies
    )

    average_gross = round(
        total_gross / total_releases,
        1
    ) if total_releases > 0 else 0

    highest_gross_movie = max(
        report_movies,
        key=lambda x: x["gross_collection"]
    ) if report_movies else None

    best_opening_movie = max(
        report_movies,
        key=lambda x: x["opening_weekend"]
    ) if report_movies else None

    return {
        "summary": {
            "month": month,
            "total_releases": total_releases,
            "total_gross_collection": total_gross,
            "average_gross_collection": average_gross,
            "highest_grossing_film": highest_gross_movie["film"] if highest_gross_movie else None,
            "highest_gross": highest_gross_movie["gross_collection"] if highest_gross_movie else 0,
            "best_opening_weekend_film": best_opening_movie["film"] if best_opening_movie else None,
            "best_opening_weekend": best_opening_movie["opening_weekend"] if best_opening_movie else 0
        },
        "movies": report_movies
    }


if __name__ == "__main__":
    app.run(debug=True)