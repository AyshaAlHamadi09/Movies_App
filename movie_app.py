import statistics
import random
from new_project.movie_project._static import movie_storage


class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def _command_list_movies(self):
        movies = self._storage.list_movies()
        print(f"Displaying {len(movies)} movies: ")
        for movie, details in movies.items():
            print(f"{movie}: {details['Rating']} - {details['Year of release']}")

    def _command_movie_stats(self):
        movies = self._storage.list_movies()
        self.stats(movies)

    def _command_add_movie(self):
        title = str(input("Enter a movie you want to add: "))
        movies = self._storage.list_movies()
        if self._storage.add_movie(title) == False:
            print("Error")
        elif title in movies:
            print(f"Movie {title} already exists!")
        else:
            self._storage.add_movie(title)
            print(f"{title} is successfully added to the movie database")

    def _command_delete_movie(self):
        title = str(input("Enter a movie you want to delete: "))
        movies = self._storage.list_movies()
        if title in movies:
            self._storage.delete_movie(title)
            print(f"{title} is successfully deleted from the movie database")
        else:
            print("The movie you entered does not exist in this database")

    def _command_update_movie(self):
        movies = self._storage.list_movies()
        title = str(input("Enter a movie you want to update: "))
        if title in movies:
            rating = float(input("Enter new movie rating (0-10): "))
            self._storage.update_movie(title, rating)
            print(f"The rating of the movie:({title}) is successfully updated")
        else:
            print("The movie you entered does not exist in this database")

    def _command_generate_website(self):
        movies = self._storage.list_movies()
        self.generate_website(movies)

    def run(self):
        while True:
            print("""
Menu:
0. Exit
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Generate website
""")
            user_selection = int(input("Enter choice (0-9): "))
            if user_selection == 0:
                print("Bye!")
                break
            elif user_selection == 1:
                self._command_list_movies()
            elif user_selection == 2:
                self._command_add_movie()
            elif user_selection == 3:
                self._command_delete_movie()
            elif user_selection == 4:
                self._command_update_movie()
            elif user_selection == 5:
                self._command_movie_stats()
            elif user_selection == 6:
                self.random_movie()
            elif user_selection == 7:
                self.search_movie()
            elif user_selection == 8:
                self.sort_movies_by_rating()
            elif user_selection == 9:
                self._command_generate_website()
            else:
                print("Selection not in range. Please enter a number 0-9")

    def stats(self, dict_of_movies):
        list_of_ratings = []
        for movie in dict_of_movies:
            list_of_ratings.append(float(dict_of_movies[movie]['Rating']))
        average_rating = sum(list_of_ratings) / len(list_of_ratings)
        median_rating = statistics.median(list_of_ratings)
        # Find the best movie according to rating
        best_movie = max(dict_of_movies, key=lambda x: float(dict_of_movies[x]["Rating"]))
        highest_rating = float(dict_of_movies[best_movie]["Rating"])
        # Find the worst movie according to rating
        worst_movie = min(dict_of_movies, key=lambda x: float(dict_of_movies[x]["Rating"]))
        lowest_rating = float(dict_of_movies[worst_movie]["Rating"])
        print(f"""Average rating: {average_rating}
Median rating: {median_rating}
Best movie: {best_movie}, rated {highest_rating}
Worst movie: {worst_movie}, rated {lowest_rating}""")

    def random_movie(self):
        movies = self._storage.list_movies()
        random_movie_pick = random.choice(list(movies.keys()))
        movie_rating = movies[random_movie_pick]['Rating']
        print(f"Your movie for tonight is {random_movie_pick}. It is rated {movie_rating}.")

    def search_movie(self):
        movies = self._storage.list_movies()
        name_entered = str(input("Enter part of the movie name: ")).lower()
        found_movies = []
        for movie, details in movies.items():
            if name_entered in movie.lower():
                found_movies.append(movie)
        if found_movies:
            for movie in found_movies:
                print(f"{movie}: {movies[movie]['Rating']}")
        else:
            print("Sorry, no movies matching the search criteria were found in this database")

    def sort_movies_by_rating(self):
        movies = self._storage.list_movies()
        sorted_movies = sorted(movies.items(), key=lambda x: float(x[1]["Rating"]), reverse=True)
        for movie, info in sorted_movies:
            print(movie, "-", float(info["Rating"]))

    def generate_website(self, dict_of_movies):
        html_string = ""
        for movie, movie_info in dict_of_movies.items():
            try:
                movie_html = f"""<li><div class="movie"><img class="movie-poster"src="{movie_info['Poster Image URL']}"/><div class="movie-title">{movie}</div><div class="movie-year">2008</div></div></li>"""
                html_string += movie_html
            except KeyError:
                pass
        with open("index_template.html", "r") as fileobj:
            orig_html_template = fileobj.read()
        with open("new_html.html", "w") as fileobj:
            new_html = orig_html_template.replace("__TEMPLATE_MOVIE_GRID__", html_string)
            new_html = new_html.replace("__TEMPLATE_TITLE__", "My Movies Website")
            fileobj.write(new_html)
        print("Website generated successfully")

if __name__ == "__main__":
    app = MovieApp(movie_storage)
    app.run()
