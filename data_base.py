from typing import List, Tuple
from handlers import Hotel
import sqlite3
import os


class Request:
    """
    Class that describes the user request

    Args:
        request_id (int): Request ID
        command (str): command the user used to get hotels
        date (str): date and time of the request
        hotels (List[Hotel]): the list of hotels from this request

    """
    def __init__(self, request_id: int, command: str, city: str, date: str, hotels: List[Hotel]) -> None:
        self.id: int = request_id
        self.command: str = command
        self.date: str = date
        self.hotels: List[Hotel] = hotels
        self.city = city

    def __str__(self) -> str:
        hotels_names: str = '\n• '.join(map(lambda x: x.name, self.hotels))
        return '✅ The result of the request based on the {command} command in {city} at {date}:\n• {result}'.format(
            command=self.command, city=self.city, date=self.date, result=hotels_names
        )


class DataBase:
    """
    Class that controls and manages the database 

    Args:
        filename (str): the filename of database
    
    Attributes:
        conn: connection to a database
        cursor: connection cursor

    """
    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.conn = None
        self.cursor = None

    def start(self) -> None:
        """
        Method that starts the database
        :return: None
        """
        self.conn = sqlite3.connect(self.filename)
        self.cursor = self.conn.cursor()

    def close(self) -> None:
        """
        Method that closes the database
        :return: None
        """
        try:
            self.conn.close()
        except AttributeError:
            pass

    def clear(self) -> None:
        """
        Methods that clears the database
        :return: None
        """
        try:
            self.close()
            os.remove(self.filename)
            self.conn = sqlite3.connect(self.filename)
            self.cursor = self.conn.cursor()
            self.create()
            print('The database was successfully cleared!')
        except PermissionError:
            print('The Exception occurred! Please close the database and try again!')

    def create(self) -> None:
        """
        Method that generates all tables in database
        :return: None
        """
        self.cursor.execute("""CREATE TABLE hotels (
                hotelId char UNIQUE NOT NULL,
                name char NOT NULL,
                address char NOT NULL,
                price char NOT NULL,
                rating integer NOT NULL,
                distance char NOT NULL
            )""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE requests (
                requestId integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                userId integer NOT NULL,
                command char NOT NULL,
                city char NOT NULL,
                time DATE DEFAULT (DATETIME('now')) NOT NULL,
                hotels text NOT NULL
            )""")
        self.conn.commit()

    def insert_hotel(self, hotel: Hotel) -> None:
        """
        Method that inserts the hotel to the database

        :param hotel: the instance of the hotel class that needs to be inserted
        :type hotel: Hotel
        :return: None
        """
        try:
            self.cursor.execute(
                "INSERT INTO hotels VALUES (:hotelId, :name, :address, :price, :rating, :distance)",
                {'hotelId': hotel.id, 'name': hotel.name, 'address': hotel.address, 'price': hotel.price,
                 'rating': hotel.rating, 'distance': hotel.distance}
            )
        except sqlite3.IntegrityError:
            pass
        finally:
            self.conn.commit()

    def insert_request(self, user_id: int, command: str, city: str, hotels: List[Hotel]) -> None:
        """
        Method that inserts the user request to the database 

        :param user_id: User ID who requested hotels 
        :type user_id: int
        :param command: command of the request
        :type command: str
        :param city: city of the request
        :type city: str
        :param hotels: the list of hotels produced by the request
        :type hotels: List[Hotel]
        :return: None
        """
        for i_hotel in hotels:
            self.insert_hotel(i_hotel)
        self.cursor.execute(
            "INSERT INTO requests ('userId', 'command', 'city', 'hotels') VALUES (:userId, :command, :city, :hotels)",
            {'userId': str(user_id), 'command': command, 'city': city, 'hotels': ', '.join(
                map(lambda x: str(x.id), hotels))
             }
        )
        self.conn.commit()

    def get_hotel(self, hotel_id: str) -> Hotel:
        """
        Method that gets the hotels from database based on its ID

        :param hotel_id: Hotel ID
        :type hotel_id: str
        :return: Hotel
        """
        self.cursor.execute("SELECT * FROM hotels WHERE hotelId=?", (hotel_id,))
        result: Tuple = self.cursor.fetchone()
        return Hotel(hotel_id=result[0], name=result[1], address=result[2], price=result[3], rating=result[4],
                     distance=result[5], images=None)

    def get_requests(self, user_id: int) -> List[Request]:
        """
        Method that gets the request from teh user based on their ID

        :param user_id: User ID
        :type user_id: int
        :return: final
        :rtype: List[Request]
        """
        self.cursor.execute("SELECT * FROM requests WHERE userId=?", (user_id,))
        result: List[Tuple] = self.cursor.fetchall()
        final: List[Request] = []
        for i_request in result:
            hotels: List[Hotel] = list()
            for i_hotel_id in i_request[5].split(', '):
                hotels.append(self.get_hotel(i_hotel_id))
            final.append(Request(i_request[0], i_request[2], i_request[3], i_request[4], hotels))
        final.reverse()
        return final


if __name__ == '__main__':
    db = DataBase('history.db')
    db.start()

    if input('Do you want to clear the database? ').strip().lower() == 'yes':
        db.clear()

    db.close()
