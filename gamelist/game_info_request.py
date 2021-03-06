import json, requests.exceptions
from igdb.wrapper import IGDBWrapper
from practice.local_settings import igdbapi_key
from datetime import datetime

wrapper = IGDBWrapper(igdbapi_key)


def igdbapi_search(game_title):
    try:
        byte_array = wrapper.api_request(
            'games',
            'search "' + game_title + '"; fields name, first_release_date, url, genres, storyline, summary;'
            )
        json_api_data = json.loads(byte_array)
        genres_list = []
        # Checking for emptiness
        if not json_api_data:
            return None
        else:
            useless_results = ("Collector's Edition", "Collection", "Trilogy", "Golden Edition", "Legacy Collection")
            for result in json_api_data:
                # Checking for useless results
                for useless in useless_results:
                    if useless in result["name"]:
                        result.clear()
                        break
                else:
                    if 'first_release_date' in result:
                         # formatting date from unix to default format
                        formated_date = datetime.fromtimestamp(result['first_release_date']).strftime("%d-%m-%Y")
                        result['first_release_date'] = formated_date
                    if 'genres' in result:
                        # adding genres to the list
                        genres_list.append(result['genres'])
            merged_genres_list = []
            for list in genres_list:
                merged_genres_list.extend(list)
            # initially the request gives me only an id of genres, so i have to make another request to find out the names
            byte_array = wrapper.api_request(
                'genres',
                'fields name; where id = (' + ','.join(map(str, merged_genres_list)) + ');'
                )
            json_api_genres = json.loads(byte_array)
            # replacing id to names of genres
            for result in json_api_data:
                if 'genres' in result:
                    counter = 0
                    for id in result['genres']:
                        for genre_name in json_api_genres:
                            if id == genre_name['id']:
                                result['genres'][counter] = genre_name['name']
                                counter += 1
                    result['genres'] = ', '.join(map(str, result['genres']))
                # if the game is blank
                if 'genres' and 'first_release_date' not in result:
                    result.clear()
            print(json_api_data)
            return json_api_data
    except requests.exceptions.RequestException:
            return None


def igdbapi_getinfo(game_id):
    try:
        byte_array = wrapper.api_request(
            'games',
            'fields name, url; where id =' + ' ' + str(game_id) + ';'
            )
        json_api_game_data = json.loads(byte_array)
        return json_api_game_data
    except requests.exceptions.RequestException:
        return None
