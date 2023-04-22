from typing import List, Dict, Tuple, Optional, Union
from dotenv import load_dotenv
from handlers import Hotel
import requests
import json
import os


class HotelRequests:
    """ Class executing the requests to Hotels API """

    def __init__(self) -> None:
        load_dotenv()
        self.__x_rapidapi_key: str = os.getenv('x_rapidapi_key')
        self.__headers: Dict[str: str] = {
            "content-type": "application/json",
            "X-RapidAPI-Key": self.__x_rapidapi_key,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    def get_property_details(self, hotelId):
        # ! DATA SAVING MODE
        # return 'undefined', 'undefined' 

        url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "propertyId": str(hotelId)
        }

        response = requests.request("POST", url, json=payload, headers=self.__headers)

        save_file = open("file4.json", "w")  
        json.dump(json.loads(response.text), save_file, indent = 4)  
        save_file.close()

        if len(json.loads(response.text).get('errors', {})) != 0:
            return 'undefined', 'undefined'

        stars = json.loads(response.text).get('data', {}).get('propertyInfo', {}).get('summary', {}).get('overview', {}).get('propertyRating', {}).get('rating')
        address = json.loads(response.text).get('data', {}).get('propertyInfo', {}).get('summary', {}).get('location', {}).get('address', {}).get('addressLine')

        return stars, address

    def get_hotels(self, destination_id: str, number: int, sort: str, images_num: int,
                   cost_range: Optional[Tuple[str]] = None, distance_range: Optional[Tuple[str]] = None) -> List[Hotel]:
        """
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
        :type cost_range: Optional[Tuple[str]
        :param distance_range: Tuple that contains the range of the possible distance from the center.
            1st value - minimal distance, 2nd - maximum distance
        :type distance_range: Optional[Tuple[str]

        :return: hotels_list
        :rtype: List[Hotel
        """

        def get_neighborhood(obj):
            if obj == None:
                return 'Undefined'
            return obj.get('name')
        
        url = "https://hotels4.p.rapidapi.com/properties/v2/list"

        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "destination": {"regionId": str(destination_id)},
            "checkInDate": {
                "day": 10,
                "month": 10,
                "year": 2022
            },
            "checkOutDate": {
                "day": 15,
                "month": 10,
                "year": 2022
            },
            "rooms": [
                {
                    "adults": 2,
                    "children": []
                }
            ],
            "resultsStartingIndex": 0,
            "resultsSize": int(number),
            "sort": sort
        }
        
        response = requests.request("POST", url, json=payload, headers=self.__headers)
        hotels = json.loads(response.text).get('data', {}).get('propertySearch', {}).get('properties', {})

        # hotels_list = list(
        #     map(
        #         lambda x: Hotel(
        #             hotel_id=x.get("id"),
        #             name=x.get('name'),
        #             # address=get_neighborhood(x.get('neighborhood')),
        #             # rating=x.get('starRating', 0),
        #             # address, rating = (0, 0),
        #             price=x.get('mapMarker', {}).get('label', {}),
        #             images=[x.get('propertyImage', {}).get('image', {}).get('url')],
        #             distance=0
        #         ), hotels
        #     )
        # )
        hotels_list = []
        for hotel in hotels:
            hotel_id=hotel.get("id")
            name=hotel.get('name')
            rating, address = self.get_property_details(str(hotel_id))
            price=hotel.get('mapMarker', {}).get('label', {})
            images=[hotel.get('propertyImage', {}).get('image', {}).get('url')]
            distance=0

            hotels_list.append(
                Hotel(
                    hotel_id=hotel_id,
                    name=name,
                    address=address,
                    rating=rating,
                    price=price,
                    images=images,
                    distance=distance
                )
            )
        return hotels_list

    def get_destination_id(self, city: str) -> str:
        """
        Method getting the City ID based on its name.
        if the city is not found returns the string 'CITY_NOT_FOUND'

        :param city: City name
        :type city: str
        :return: destination_id
        :rtype: str
        :return: 'CITY_NOT_FOUND'
        :rtype: str
        """
        url: str = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring = {"q": city,"locale":"en_US","langid":"1033","siteid":"300000001"}
        response: dict = json.loads(requests.request("GET", url, headers=self.__headers, params=querystring).text)

        destination_id: Optional[str] = None
        try:
            destination_id = str(response['sr'][0]['essId'].get('sourceId'))
        except IndexError:
            destination_id = 'CITY_NOT_FOUND'
        finally:
            return destination_id

    def get_photos(self, hotel_id: str, num: Union[str, int]) -> Optional[List[str]]:
        """
        Method getting the pictures of hotels

        :param hotel_id: Hotel ID
        :type hotel_id: str
        :param num: Number of pictures for each hotel
        :type num: Union[str, int]
        :returns: (result, None)
        :rtype: Optional[List[str]]
        """
        if int(num) == 0:
            # If images are not needed
            return
        url: str = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
        querystring: Dict[str] = {"id": hotel_id}

        response: dict = json.loads(requests.request("GET", url, headers=self.__headers, params=querystring).text)
        result: list[str] = list(map(
            lambda x: x['baseUrl'].format(size=x['sizes'][0]['suffix']),
            response['hotelImages']
        ))[:int(num)]

        return result



if __name__ == '__main__':
    
    hotelsR = HotelRequests()

    # print(hotelsR.get_destination_id('New York')) # -> 2621

    # hotels = hotelsR.get_hotels('2621', 3, 'PRICE_LOW_TO_HIGH', 1, (100, 150), (0,0))

    # for h in hotels:
    #     print(f'{h.id}:\n{h}\nImage: {h.images}\n\n')

    # print(hotelsR.get_property_details('8865'))
