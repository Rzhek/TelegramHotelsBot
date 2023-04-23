# <span id="top">Telegram Bot for Hotel Search </span>
![alt-text](img/preview.gif 'preview')

Create a **Telegram Bot** to work with *hotels*!
___

External Libraries

- pyTelegramBotAPI
- python-dotenv
- requests

```
pip install -r requirements.txt
```
___

## Sample Code
Firstly, create an instance of **Bot** Class, passing your *token* as an argument
````python
bot = Bot(TOKEN)
````
___

Then, create a **function**, that has to take message as argument and wrap it with a decorator *bot.message_handler()*  
You need to pass a *content_types* argument to a decorator. *Pass \['text'\] to make bot listen to all messages*

````python
@bot.message_handler(content_types=['text'])
def reply(message) -> None:
    pass
````
___

After than, everything is built with conditional statements, message variable, and bot's methods
*Generally speaking, if got this message - call that method*

```python
@bot.message_handler(content_types=['text'])
def reply(message) -> None:
    if message.text == '/your_command':
        your_method()
```

___
Finally, start your bot with this command:

```python
bot.polling(none_stop=True, interval=0)
```

> Done! Now the bot will answer your messages!

<br/>

**Important Note:**

Due to the release of new API version, some previous features are currently not working. The whole Request System was rebuilt, and most features could be kept, while other cannot be implemented with new API structure (at least for now). Therefore, it was decided to temporally turn off some features, mostly related to the /bestdeal command 

<br/>


## Classes, methods, and functions information

In this section, the **detailed information** about *classes, their methods nad functions* will be provided

### Class Bot

````
    Args:
        token (str): Bot token

    Attributes:
        requests (HotelRequests): Instance of the class, executing requests to hotels API
        database (DataBase): Instance of the class that controls and manages the requests history database
        info (Optional[Dict[str, Optional[str, int]]]): Dictionary of user's request criteria
````

#### **Method clear_data**
````
    Method clearing the criteria of the request

    :return: None
````

#### **Method send_info**
````
    Method that sends the list of commands to the user

    :param chat_id: Chat id in which the message needs to be sent
    :type chat_id: int
    :return: None
````

#### **Method send_hotels**
````
    Method that send the list of hotels to the user

    :param chat_id: Chat id in which the message needs to be sent
    :type chat_id: int
    :param hotels: List of hotels
    :type hotels: List[handlers.Hotel]
    :return: None
````

#### **Method say_hello**
````
    Method greeting the user

    :param user: The user, bot has to greet
    :return: None
````

#### **Method send_low_hotels**
````
    Method starting a branch to find low price hotels

    :param chat_id: Chat id in which the message needs to be sent
    :type chat_id: int
    :return: None
````

#### **Method send_high_hotels**
````
    Method starting a branch to find high price hotels

    :param chat_id: Chat id in which the message needs to be sent
    :type chat_id: int
    :return: None
````

#### **Method send_best_hotels**
> Currently is not being used
````
    Method starting a branch to find best price hotels based on the cost and distance from the center 

    :param chat_id: Chat id in which the message needs to be sent
    :type chat_id: int
    :return: None
````

#### **Method send_history**
````
    Method sending the history of requested hotels to the user

    :param chat_id: Chat id in which the message needs to be sent
    :type chat_id: int
    :return: None
````


___
___ 
### Class Hotel
````
    Args:
        hotel_id (str): Hotel's ID
        name (str): Hotel's name
        address (str): Hotel's address
        price (str): Hotel's price
        rating (str): Hotel's rating
        images (Optional[List[str]]): Hotel's pictures
        distance (str): Hotel's distance from center
````

___
___
### Class HotelRequests

````
    Class executing the requests to Hotels API

        Args:
            __x_rapidapi_key (str): the personal API key
            __headers (Dict[str: str]): settings for API requests    
````

#### **Method get_property_details**
```
    Methods that makes a request to the API to get the rating and address from the hotel

    :param hotelId: Hotel ID
    :type hotelId: str
    :return: Tuple[Union[str, int], str]
```

#### **Method get_hotels**
> Currently, some of the arguments are not processed and do not affect the final result (images_num, cost_range, distance_range)
````
    Final method that gets the hotels based on all criteria

    :param destination_id: City ID 
    :type destination_id: str
    :param number: Number of hotels
    :type number: str
    :param sort: Sorting method
        Can be one of 3 values: "PRICE", "PRICE_HIGHEST_FIRST", or "DISTANCE_FROM_LANDMARK"
    :type sort: str
    :param images_num: Number of pictures for each hotel 
    :type images_num: int
    :param cost_range: Tuple that contains the range of possible prices.
        1st value - minimal price, 2nd - maximum price
    :type cost_range: Optional[Tuple[str]]
    :param distance_range: Tuple that contains the range of the possible distance from the center.
        1st value - minimal distance, 2nd - maximum distance
    :type distance_range: Optional[Tuple[str]]

    :return: hotels_list
    :rtype: List[Hotel]
````

#### **Method get_destination_id**
````
    Method getting the City ID based on its name.
    if the city is not found returns the string 'CITY_NOT_FOUND'

    :param city: City name
    :type city: str
    :return: destination_id
    :rtype: str
    :return: 'CITY_NOT_FOUND'
    :rtype: str
````

#### **Method get_photos**

> Currently is not being used

````
    Method getting the pictures of hotels

    :param hotel_id: Hotel ID
    :type hotel_id: str
    :param num: Number of pictures for each hotel
    :type num: Union[str, int]
    :returns: (result, None)
    :rtype: Optional[List[str]]
````


___
___
### Class Request
```` 
    Class that describes the user request

    Args:
        request_id (int): Request ID
        command (str): command the user used to get hotels
        date (str): date and time of the request
        hotels (List[Hotel]): the list of hotels from this request
````


___
___
### Class DataBase
```` 
    Class that controls and manages the database 

    Args:
        filename (str): the filename of database
    
    Attributes:
        conn: connection to a database
        cursor: connection cursor
````

#### **Method start**
````
    Method that starts the database
    :return: None
````

#### **Method close**
````
    Method that closes the database
    :return: None
````

#### **Method clear**
````
    Methods that clears the database
    :return: None
````

#### **Method create**
````
    Method that generates all tables in database
    :return: None
````

#### **Method insert_hotel**
````
    Method that inserts the hotel to the database

    :param hotel: the instance of the hotel class that needs to be inserted
    :type hotel: Hotel
    :return: None
````

#### **Method insert_request**
````
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
````

#### **Method get_hotel**
````
    Method that gets the hotels from database based on its ID

    :param hotel_id: Hotel ID
    :type hotel_id: str
    :return: Hotel
````

#### **Method get_request**
````
    Method that gets the request from teh user based on their ID

    :param user_id: User ID
    :type user_id: int
    :return: final
    :rtype: List[Request]
````


___
___
### Handler Functions
```` 
Functions used to process messages and redirect the user to another branch of dialog
````
#### **Function select_city**
````
    Function that gets the City ID and redirects to the branch of choosing number of hotels 

    :param message: User message that contains the city name
    :param bot: Instance of Bot class
    :return: None
````

#### **Function select_cost_range** 
> Currently is not being used
````
    Function that gets the price range from the user and redirects to the branch of choosing the range of the possible distance from center 

    :param message: User message that contains the range of prices
    :param bot: Instance of Bot class
    :return: None
````

#### **select_distance_range **
> Currently is not being used
````
    Function that gets the range of possible distance and redirects to the branch of choosing the number of hotels 

    :param message: User message that contains the range of distances
    :param bot: Instance of Bot class
    :return: None
````

#### **Function select_hotel_number**
````
    Function that gets the number of hotels from user and send the list of hotels to user 

    :param message: User message that contains the number of hotels
    :param bot: Instance of Bot class
    :return: None
````

#### **Function images_need**
> Currently is not being used
````
    Function that gets the information whether or not the user needs images and redirects tot the branch of choosing the number of images or send hotels to the user

    :param message: User message that contains the answer (yes / no)
    :param bot: Instance of Bot class
    :return: None
````

#### **Function select_images_num**
> Currently is not being used
````
    Function that gets the number of images and send hotels to the user

    :param message: User message that contains the number of images
    :param bot: Instance of Bot class
    :return: None
````

___

<a href="#top">On top</a>
