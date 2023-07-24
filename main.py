from movie_app import MovieApp
from storage_json import StorageJson


def main():
    storage = StorageJson('_static/movies.json')
    main_movie_app = MovieApp(storage)
    main_movie_app.run()



if __name__ == '__main__':
    main()