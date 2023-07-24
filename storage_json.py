from istorage import IStorage
import json
import requests

class StorageJson(IStorage):
    def __init__(self, file_path="movie_data.json"):
        self.file_path = file_path

    def list_movies(self):
        try:
            with open(self.file_path, "r") as fileobj:
                data = fileobj.read()
                movie_dict = json.loads(data)
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

        movie_dict = self.list_movies()
        movie_dict[title] = {}
        movie_dict[title]['Year of release'] = movie_info['Year']
        movie_dict[title]['Rating'] = movie_info['imdbRating']
        movie_dict[title]['Poster Image URL'] = movie_info['Poster']

        try:
            with open(self.file_path, "w") as fileobj:
                fileobj.write(json.dumps(movie_dict))
        except FileNotFoundError:
            print(f"File '{self.file_path}' not found. Unable to save data.")
            return False

        return True

    def delete_movie(self, title):
        movie_dict = self.list_movies()
        if title in movie_dict:
            del movie_dict[title]
            try:
                with open(self.file_path, "w") as fileobj:
                    fileobj.write(json.dumps(movie_dict))
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
                with open(self.file_path, "w") as fileobj:
                    fileobj.write(json.dumps(movie_dict))
            except FileNotFoundError:
                print(f"File '{self.file_path}' not found. Unable to save data.")
                return False
            return True
        else:
            print(f"Movie '{title}' not found in the storage.")
            return False



if __name__ == "__main__":
    storage = StorageJson()


#TESTING
    print("Test 1: Adding a movie to the storage")
    print(storage.add_movie("Inception", year=2010, rating=8.8, poster="https://example.com/poster.jpg"))


    print("Test 2: Listing movies after adding one")
    print(storage.list_movies())

    print("Test 3: Updating the rating of a movie")
    storage.update_movie("Inception", rating=9.0, notes="Great movie!")
    print(storage.list_movies())


    print("Test 5: Deleting a movie from the storage")
    storage.delete_movie("Inception")
    print(storage.list_movies())

