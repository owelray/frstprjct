import requests, json
from igdb.wrapper import IGDBWrapper
from practice.local_settings import igdbapi_key
from datetime import datetime

wrapper = IGDBWrapper(igdbapi_key)

def igdbapi_search(game_title):
    byte_array = wrapper.api_request(
        'games',
        'search "' + game_title + '"; fields name, first_release_date, url, genres, storyline, summary;'
        )
    json_api_data = json.loads(byte_array)
    genres_list = []

    for result in json_api_data:
        if "Collector's Edition" in result['name']:
            result.clear()
        else:
            if "Collection" in result['name']:
                result.clear()
            else:
                if "Trilogy" in result['name']:
                    result.clear()
                else:
                    if 'first_release_date' in result:
                        formated_date = datetime.fromtimestamp(result['first_release_date']).strftime("%d-%m-%Y")
                        result['first_release_date'] = formated_date
                    if 'genres' in result:
                        genres_list.append(result['genres'])
    merged_genres_list = []
    for list in genres_list:
        merged_genres_list.extend(list)
    byte_array = wrapper.api_request(
        'genres',
        'fields name; where id = ('+ ','.join(map(str, merged_genres_list)) +');'
        )
    json_api_genres = json.loads(byte_array)
    for result in json_api_data:
        if 'genres' in result:
            counter = 0
            for id in result['genres']:
                for genre_name in json_api_genres:
                    if id == genre_name['id']:
                        result['genres'][counter] = genre_name['name']
                        counter += 1
            result['genres'] = ', '.join(map(str, result['genres']))
        if 'genres' and 'first_release_date' not in result:
            result.clear()
    return json_api_data

def igdbapi_getinfo (game_id):
    byte_array = wrapper.api_request(
        'games',
        'fields name, url; where id =' + ' ' + str(game_id) + ';'
        )
    json_api_game_data = json.loads(byte_array)
    return json_api_game_data








