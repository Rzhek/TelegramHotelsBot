from typing import Optional, List

max_hotels: int = 15
max_images: int = 10


class Hotel:
    """
    Class describing a hotel

    Args:
        hotel_id (str): Hotel's ID
        name (str): Hotel's name
        address (str): Hotel's address
        price (str): Hotel's price
        rating (str): Hotel's rating
        images (Optional[List[str]]): Hotel's pictures
        distance (str): Hotel's distance from center

    """
    def __init__(self, hotel_id: str, name: str, address: str, price: str, rating: str, images: Optional[List[str]],
                 distance: str) -> None:
        self.id: str = hotel_id
        self.name: str = name
        self.address: str = address
        self.price: str = price
        self.rating: str = rating
        self.images: Optional[List[str]] = images
        self.distance: str = distance

    # def __str__(self) -> str:
    #     rating: str = '⭐️' * int(self.rating)
    #     return '🏨 Hotel: {name}\n💵 Price: {price}\n🌟 Rating: {rating}\n📐 Distance from the center: {distance}\n' \
    #            '🗺 Address: {address}'.format(
    #                 name=self.name, price=self.price, rating=rating, distance=self.distance, address=self.address
    #             )

    def __str__(self) -> str:
        if self.rating == 'undefined':
            rating = self.rating
        else:
            rating: str = ('⭐️' * int(round(self.rating, 0))) if self.rating >= .5 else '0'
        return '🏨 Hotel: {name}\n💵 Price: {price}\n🌟 Rating: {rating}\n' \
               '🗺 Address: {address}'.format(
                    name=self.name, price=self.price, rating=rating, address=self.address
                )


def select_city(message, bot) -> None:
    """
    Function that gets the City ID and redirects to the branch of choosing number of hotels 

    :param message: User message that contains the city name
    :param bot: Instance of Bot class
    :return: None
    """
    bot.info['city_name'] = message.text
    bot.info['city'] = bot.requests.get_destination_id(message.text)
    if bot.info['city'] == 'CITY_NOT_FOUND':
        # if city was not found 
        bot.send_message(message.from_user.id, '😔 I dont have enough information about this city!')
        return
    # if bot.info['command'] != '/bestdeal':
    #     # If the /bestdeal command is not being used - ask the number of hotels
    #     msg = bot.send_message(message.from_user.id, '📝 Enter the number of hotels:')
    #     bot.register_next_step_handler(msg, select_hotels_number, bot=bot)
    else:
        # If the /bestdeal command is being used
        msg = bot.send_message(message.from_user.id, '📝 Enter the number of hotels:')
        bot.register_next_step_handler(msg, select_hotels_number, bot=bot)


# def select_cost_range(message, bot) -> None:
#     """
#     Function that gets the price range from the user and redirects to the branch of choosing the range of the possible distance from center 

#     :param message: User message that contains the range of prices
#     :param bot: Instance of Bot class
#     :return: None
#     """
#     bot.info['cost_range'] = tuple(message.text.strip().split()[:2])

#     # TODO: FIX WHEN FIND OUT A WAY TO FIND THE DISTANCE FROM THE CENTER
#     # msg = bot.send_message(message.from_user.id, '📐 Enter the range of possible distance separated by space:')
#     # bot.register_next_step_handler(msg, select_distance_range, bot=bot)
#     msg = bot.send_message(message.from_user.id, '📝 Enter the number of hotels:')
#     bot.register_next_step_handler(msg, select_hotels_number, bot=bot)


# def select_distance_range(message, bot) -> None:
#     """
#     Function that gets the range of possible distance and redirects to the branch of choosing the number of hotels 

#     :param message: User message that contains the range of distances
#     :param bot: Instance of Bot class
#     :return: None
#     """
#     bot.info['distance_range'] = tuple(message.text.split()[:2])
#     msg = bot.send_message(message.from_user.id, '📝 Enter the number of hotels:')
#     bot.register_next_step_handler(msg, select_hotels_number, bot=bot)


def select_hotels_number(message, bot) -> None:
    """
    Function that gets the number of hotels from user and send the list of hotels to user 

    :param message: User message that contains the number of hotels
    :param bot: Instance of Bot class
    :return: None
    """
    if 0 < int(message.text) <= max_hotels:
        # if the number of hotels is in possible range
        bot.info['num'] = message.text

        # ? SHOULD THIS FEATURE BE KEPT TO MAKE A SEPARATE REQUEST FOR EACH HOTEL IF NEW API ALREADY PROVIDES ONE PICTURE IN A GENERAL REQUEST 
        # msg = bot.send_message(message.from_user.id, '📷 Do you want to get the image of each hotel?')
        # bot.register_next_step_handler(msg, images_need, bot=bot)
        hotels: List[Hotel] = bot.requests.get_hotels(
            bot.info['city'], bot.info['num'], bot.info['sort'], 1,
            cost_range=bot.info['cost_range'], distance_range=(0,0)
        )
        bot.send_hotels(message.from_user.id, hotels)
    else:
        # if the number of hotels is not in possible range
        msg = bot.send_message(message.from_user.id, f'☝️ The number of hotels should not exceed {max_hotels}\n'
                                                     'Enter the number of hotels one more time:')
        bot.register_next_step_handler(msg, select_hotels_number, bot=bot)


# def images_need(message, bot) -> None:
#     """
#     Function that gets the information whether or not the user needs images and redirects tot the branch of choosing the number of images or send hotels to the user

#     :param message: User message that contains the answer (yes / no)
#     :param bot: Instance of Bot class
#     :return: None
#     """
#     if  message.text.strip().lower() == 'yes':
#         # If positive answer
#         msg = bot.send_message(message.from_user.id, '📸 How many images for each hotel you want to get?')
#         bot.register_next_step_handler(msg, select_images_num, bot=bot)
#     elif message.text.strip().lower() == 'no':
#         # if negative answer
#         hotels: List[Hotel] = bot.requests.get_hotels(
#             bot.info['city'], bot.info['num'], bot.info['sort'], bot.info['images_num'],
#             cost_range=bot.info['cost_range'], distance_range=bot.info['distance_range']
#         )
#         bot.send_hotels(message.from_user.id, hotels)
#     else:
#         # If unclear answer
#         msg = bot.send_message(message.from_user.id, '😔 I don\'t understand you. Please enter yes/no:')
#         bot.register_next_step_handler(msg, images_need, bot=bot)


# def select_images_num(message, bot) -> None:
#     """
#     Function that gets the number of images and send hotels to the user

#     :param message: User message that contains the number of images
#     :param bot: Instance of Bot class
#     :return: None
#     """
#     if 1 <= int(message.text) <= max_images:
#         # if the number of images is in possible range
#         bot.info['images_num'] = int(message.text)
#         hotels: List[Hotel] = bot.requests.get_hotels(
#             bot.info['city'], bot.info['num'], bot.info['sort'], bot.info['images_num'],
#             cost_range=bot.info['cost_range'], distance_range=bot.info['distance_range']
#         )
#         bot.send_hotels(message.from_user.id, hotels)
#     else:
#         # if the number of images is not in possible range
#         msg = bot.send_message(message.from_user.id, f'☝️ The number of images should not exceed {max_images}\n'
#                                                      'Enter the number of images one more time:')
#         bot.register_next_step_handler(msg, select_images_num, bot=bot)
