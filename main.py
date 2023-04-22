from telebot.types import InputMediaPhoto
from hotel_requests import HotelRequests
from typing import Dict, List, Optional, Union
from data_base import DataBase
from dotenv import load_dotenv
import handlers
import telebot
import os


class Bot(telebot.TeleBot):
    """
    Bot Class

    Args:
        token (str): Bot token

    Attributes:
        requests (HotelRequests): Instance of the class, executing requests to hotels API
        database (DataBase): Instance of the class that controls and manages the requests history database
        info (Optional[Dict[str, Optional[str, int]]]): Dictionary of user's request criteria

    """
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.requests = HotelRequests()
        self.database = DataBase('history.db')
        self.info: Optional[Dict[str, Optional[Union[str, int]]]] = None
        self.clear_data()

    def clear_data(self) -> None:
        """
        Method clearing the criteria of the request

        :return: None
        """
        self.info = {'city': None, 'city_name': None, 'num': None, 'sort': None, 'images_num': 1, 'cost_range': None,
                     'distance_range': None, 'command': None}

    def send_info(self, chat_id: int) -> None:
        """
        Method that sends the list of commands to the user

        :param chat_id: Chat id in which the message needs to be sent
        :type chat_id: int
        :return: None
        """
        self.send_message(chat_id, "📌 My commands:\n\n"
                                   "📉 /lowprice - show top cheap hotels\n"
                                   "💷 /highprice - show top premium hotels\n"
                                #    "📈 /bestdeal - show top optimal hotels\n"
                                   "📖 /history - show the history of requested hotels")

    def send_hotels(self, chat_id: int, hotels: List[handlers.Hotel]) -> None:
        """
        Method that send the list of hotels to the user

        :param chat_id: Chat id in which the message needs to be sent
        :type chat_id: int
        :param hotels: List of hotels
        :type hotels: List[handlers.Hotel]
        :return: None
        """
        if len(hotels) == 0:
            # if the number of hotels found is 0, tell the user that there is no hotels found for their criteria
            self.send_message(chat_id, '❌ No hotels for the given criteria were found ❌\n'
                                       'Make sure that all data are entered correctly!')
            return

        num: int = 1
        if len(hotels) == int(self.info['num']):
            # if enough hotels were found
            self.send_message(chat_id, 'Your hotels:')
        else:
            # if not enough hotels were found
            self.send_message(chat_id, '😔 Unfortunately I could not find enough hotels for you, but here are some of those I have found:')

        # sending hotels
        for i_hotel in hotels:
            msg: str = '{}) {}'.format(num, i_hotel)
            if int(self.info['images_num']) == 0:
                self.send_message(chat_id, msg)
            else:
                media: List[InputMediaPhoto] = list()
                for i_image in i_hotel.images:
                    media.append(InputMediaPhoto(i_image))
                media[0].caption = msg
                self.send_media_group(chat_id, media)
            num += 1

        # Adding the request to database
        self.database.start()
        self.database.insert_request(user_id=chat_id, command=self.info['command'], city=self.info['city_name'],
                                     hotels=hotels)
        self.database.close()
        self.clear_data()

    def say_hello(self, user) -> None:
        """
        Method greeting the user

        :param user: The user, bot has to greet
        :return: None
        """
        self.send_message(user.id, "👋 Hi, {} {}".format(user.first_name, user.last_name))

    def send_low_hotels(self, chat_id: int) -> None:
        """
        Method starting a branch to find low price hotels

        :param chat_id: Chat id in which the message needs to be sent
        :type chat_id: int
        :return: None
        """
        self.info['sort'] = 'PRICE_LOW_TO_HIGH'
        self.info['command'] = '/lowprice'
        msg = self.send_message(chat_id, '🌆 Enter your city:')
        self.register_next_step_handler(msg, handlers.select_city, bot=self)

    def send_high_hotels(self, chat_id: int) -> None:
        """
        Method starting a branch to find high price hotels


        :param chat_id: Chat id in which the message needs to be sent
        :type chat_id: int
        :return: None
        """
        self.info['sort'] = 'PRICE_HIGH_TO_LOW'
        self.info['command'] = '/highprice'
        msg = self.send_message(chat_id, '🌆 Enter your city:')
        self.register_next_step_handler(msg, handlers.select_city, bot=self)

    # def send_best_hotels(self, chat_id: int) -> None:
    #     """
    #     Method starting a branch to find best price hotels based on the cost and distance from the center 

    #     :param chat_id: Chat id in which the message needs to be sent
    #     :type chat_id: int
    #     :return: None
    #     """
    #     self.info['sort'] = 'DISTANCE_FROM_LANDMARK'
    #     self.info['command'] = '/bestdeal'
    #     msg = self.send_message(chat_id, '🌆 Enter your city:')
    #     self.register_next_step_handler(msg, handlers.select_city, bot=self)

    def send_history(self, chat_id: int) -> None:
        """
        Method sending the history of requested hotels to the user

        :param chat_id: Chat id in which the message needs to be sent
        :type chat_id: int
        :return: None
        """
        self.database.start()
        history: str = '\n\n'.join(map(lambda x: str(x), self.database.get_requests(chat_id)))
        if len(history) != 0:
            self.send_message(chat_id, '📖 Your history of requests:\n\n{}'.format(history))
        else:
            self.send_message(chat_id, '📖 Your history of requests is empty!')
        self.database.close()


if __name__ == '__main__':
    load_dotenv()
    TOKEN: str = os.getenv('TOKEN')
    bot = Bot(TOKEN)


    @bot.message_handler(content_types=['text'])
    def reply(message) -> None:
        """
        Function registering the messages from users and calling the corresponding bot method

        :param message: user message the bot has to reply to
        :return: None
        """
        if message.text.strip().lower() == '/help':
            bot.send_info(message.from_user.id)

        elif message.text.strip().lower() in ["hi", 'hello', 'hey'] or message.text.strip().lower() == '/start':
            bot.say_hello(message.from_user)

        elif message.text.strip().lower() == '/lowprice':
            bot.send_low_hotels(message.from_user.id)

        elif message.text.strip().lower() == '/highprice':
            bot.send_high_hotels(message.from_user.id)

        # elif message.text.strip().lower() == '/bestdeal':
        #     bot.send_best_hotels(message.from_user.id)

        elif message.text.strip().lower() == '/history':
            bot.send_history(message.from_user.id)

        else:
            bot.send_message(message.from_user.id, "😔 I don't understand you.\n"
                                                   "Type /help to see the list of commands")

    bot.polling(none_stop=True, interval=0)
