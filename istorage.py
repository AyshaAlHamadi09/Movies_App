from abc import ABC, abstractmethod

class IStorage(ABC):
    API_KEY = '23a3a847'

    @abstractmethod
    def list_movies(self):
        """
        Abstract method to list all movies in the storage system.

        Returns:
            list: A list of movie objects representing all the movies stored.
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """
        Abstract method to add a new movie to the storage system.

        Args:
            title (str): The title of the movie.
            year (int): The year the movie was released.
            rating (float): The rating of the movie.
            poster (str): URL or path to the movie's poster.

        Returns:
            bool: True if the movie was successfully added, False otherwise.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Abstract method to delete a movie from the storage system.

        Args:
            title (str): The title of the movie to be deleted.

        Returns:
            bool: True if the movie was successfully deleted, False otherwise.
        """
        pass

    @abstractmethod
    def update_movie(self, title, notes):
        """
        Abstract method to update a movie's information in the storage system.

        Args:
            title (str): The title of the movie to be updated.
            notes (str): Additional notes or information about the movie.

        Returns:
            bool: True if the movie information was successfully updated, False otherwise.
        """
        pass
