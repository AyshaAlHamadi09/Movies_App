import csv
import requests
from istorage import IStorage

class StorageCSV(IStorage):
    def __init__(self, file_path="movie_data.csv"):
        self.file_path = file_path

    def list_movies(self):
        try:
            with open(self.file_path, "r", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                movie_dict = {row['Title']: row for row in reader}
                return movie_dict
        except FileNotFoundError:
            return {}

    def add_movie(self, title):
        URL = f'http://www.omdbapi.com/?apikey={self.API_KEY}&t={title}'
        try:
            response = requests.get(URL)
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred")
            return False

        movie_info = response.json()
        if movie_info['Response'] == 'False':
            print(movie_info['Error'])
            return False

        fieldnames = ["Title", "Year of release", "Rating", "Poster Image URL", "Notes"]
        movie_dict = self.list_movies()
        movie_dict[title] = {
            "Title": title,
            "Year of release": movie_info['Year'],
            "Rating": movie_info['imdbRating'],
            "Poster Image URL": movie_info['Poster'],
            "Notes": ""
        }

        try:
            with open(self.file_path, "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(movie_dict.values())
        except FileNotFoundError:
            print(f"File '{self.file_path}' not found. Unable to save data.")
            return False

        return True

    def delete_movie(self, title):
        movie_dict = self.list_movies()
        if title in movie_dict:
            del movie_dict[title]

            try:
                with open(self.file_path, "w", newline="") as csvfile:
                    fieldnames = ["Title", "Year of release", "Rating", "Poster Image URL", "Notes"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(movie_dict.values())
            except FileNotFoundError:
                print(f"File '{self.file_path}' not found. Unable to save data.")
                return False

            return True
        else:
            print(f"Movie '{title}' not found in the storage.")
            return False

    def update_movie(self, title, rating, notes=''):
        movie_dict = self.list_movies()
        if title in movie_dict:
            movie_dict[title]['Rating'] = rating
            movie_dict[title]['Notes'] = notes

            try:
                with open(self.file_path, "w", newline="") as csvfile:
                    fieldnames = ["Title", "Year of release", "Rating", "Poster Image URL", "Notes"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(movie_dict.values())
            except FileNotFoundError:
                print(f"File '{self.file_path}' not found. Unable to save data.")
                return False

            return True
        else:
            print(f"Movie '{title}' not found in the storage.")
            return False


if __name__ == "__main__":
    storage = StorageCSV()

    print("Test 1: Adding a movie to the storage")
    print(storage.add_movie("Inception"))

    print("Test 2: Listing movies after adding one")
    print(storage.list_movies())

    print("Test 3: Updating the rating of a movie")
    storage.update_movie("Inception", rating=9.0, notes="Great movie!")
    print(storage.list_movies())

    print("Test 4: Deleting a movie from the storage")
    storage.delete_movie("Inception")
    print(storage.list_movies())
