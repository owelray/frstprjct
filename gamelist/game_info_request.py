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
    # json_api_data = [{'id': 17, 'first_release_date': 984614400, 'genres': [12, 15, 16, 24], 'involved_companies': [5221, 5222], 'name': 'Fallout Tactics: Brotherhood Of Steel'}, {'id': 45128, 'first_release_date': 1138752000, 'genres': [12, 15, 31], 'name': 'Fallout Trilogy'}, {'id': 14, 'first_release_date': 907113600, 'genres': [12, 16], 'involved_companies': [4152, 4153], 'name': 'Fallout 2', 'storyline': "In 2241, the primitive Arroyo suffers the worst drought on record. Faced with the calamity, the village elder asks the direct descendant of the Vault Dweller, referred to as the Chosen One, to perform the quest of retrieving a Garden of Eden Creation Kit (GECK) for Arroyo. The GECK is a device that can create thriving communities out of the post-apocalyptic wasteland.[3] The player, assuming the role of the Chosen One, is given nothing more than the Vault Dweller's jumpsuit, a RobCo PIPBoy 2000 handheld device, a Vault 13 water flask, a spear and some cash to start on his mission."}, {'id': 13, 'first_release_date': 875577600, 'genres': [12, 16], 'involved_companies': [7806, 7807, 7808], 'name': 'Fallout', 'storyline': 'Fallout is set in the timeline which deviated from our own some time after World War II, and where technology, politics and culture followed a different course. In the 21st century, a worldwide conflict is brought on by global petroleum shortage. Several nations begin warring with one another for the last of non-renewable resources, namely oil and uranium; known as the Resource Wars, fighting begins in April 2052 and ends in 2077. China invades Alaska in the winter of 2066, causing the United States to go to war with China and using Canadian resources to supply their war efforts, despite Canadian complaints. Eventually the United States violently annexes Canada in February 2076 and reclaims Alaska nearly a year later. After years of conflict, on October 23, 2077, a global nuclear war occurs. It is not known who strikes first, but in less than a few hours most major cities are destroyed. The effects of the war do not fade for the next hundred years and as a consequence, human society has collapsed leaving only survivor settlements barely able to make out a living in the barren wasteland, while a few live through the occurrence in underground fallout shelters known as Vaults. One of these, Vault 13, is the protagonist\'s home, where the game begins. \n \nIn Vault 13, in 2161 in Southern California, 84 years after the nuclear war. The Water Chip, a computer chip responsible for the water recycling and pumping machinery, breaks. The Vault Overseer tasks the protagonist, the Vault Dweller, with finding a replacement. He or she is given a portable device called the "Pip-Boy 2000" that keeps track of map-making, objectives, and bookkeeping. Armed with the Pip-Boy 2000 and meager equipment, including a small sum of bottle caps which are used as currency in the post-apocalyptic world, the main character is sent off on the quest.'}, {'id': 122725, 'first_release_date': 1571961600, 'genres': [5, 12, 31], 'involved_companies': [95239], 'name': 'Fallout: Legacy Collection'}, {'id': 77192, 'genres': [12], 'name': 'Fallout Online'}, {'id': 15, 'first_release_date': 1225152000, 'genres': [5, 12], 'involved_companies': [4154, 4156, 95336], 'name': 'Fallout 3', 'storyline': 'The introductory sequence introduces the player to their character\'s father James, a doctor and scientist in Vault 101. James frequently makes comments about the player character\'s deceased mother Catherine, and her favorite Bible passage, Revelation 21:6, which speaks of "the waters of life". \n \nThe main quest begins after the player is forced to flee Vault 101 when James leaves the vault, throwing it into anarchy and causing the paranoid Overseer to send his security force after the player. The search for James takes the character on a journey through the Wasteland, first to the nearby town of Megaton, named for the undetonated atomic bomb at the center of town, then the Galaxy News Radio station, whose enthusiastic DJ Three Dog gives the player the moniker of "The Lone Wanderer". The player travels to Rivet City, a derelict aircraft carrier now serving as a fortified human settlement. Here the player meets Doctor Li, a scientist who worked alongside the player\'s father. Doctor Li informs the player of Project Purity, a plan conceived by Catherine and James to purify all the water in the Tidal Basin and eventually the entire Potomac River with a giant water purifier built in the Jefferson Memorial. However, continued delays and Catherine\'s death during childbirth put an end to the project, and James took the player\'s character as a newborn to raise them in the safety of Vault 101. \nAfter investigating the Jefferson Memorial, the Lone Wanderer tracks James to Vault 112, and frees him from a virtual reality program being run by the Vault\'s sadistic Overseer, Dr. Braun. James and the player return to Rivet City, and James reveals he sought out Braun for information on the Garden of Eden Creation Kit (G.E.C.K.), a device that contains the components needed to finally activate Project Purity. James and Doctor Li lead a team of Rivet City scientists to the memorial with intent to restart the project, but the memorial is invaded by the Enclave, a powerful military organization formed from the remnants of the pre-War United States government. James floods the project\'s control room with radiation to stop the Enclave military leader, Colonel Augustus Autumn, from taking control of it, killing himself (but Autumn survives), his last words urging his child to run. The Lone Wanderer and Dr. Li flee to the ruins of the Pentagon, now a base for the Brotherhood of Steel and now known as the Citadel. With Project Purity still inoperational even with the Enclave occupying the site, the player travels to Vault 87 to find a G.E.C.K. and finish James\'s work. The player finds the Vault to be a testing site for the FEV (Forced Evolutionary Virus), and the source of the Super Mutants in the Capital Wasteland. After the player acquires the G.E.C.K., the Wanderer is ambushed by the Enclave and captured. \nAt the Enclave base at Raven Rock, the player is freed from their cell by the Enclave leader, President John Henry Eden, who requests a private audience with them. En route to his office however, Colonel Autumn defies Eden\'s orders and takes command of the Enclave military, ordering them to kill the player. Fighting their way to Eden\'s office, the player discovers Eden is actually a sentient ZAX series supercomputer who took control of the Enclave after their defeat in Fallout 2 on the West Coast thirty years ago. Eden wishes to repeat the plan of then-President Dick Richardson using Project Purity, infecting the water with a modified strain of FEV that will make it toxic to any mutated life. This plan will kill most life in the wasteland including humans, but the Enclave, due to their genetic "purity" as a result of their isolation, will be immune and free to take control of the area. The Wanderer, provided with a sample of the new F.E.V., is given a choice to either leave peacefully or convince Eden to self-destruct the entire base. The Lone Wanderer escapes Raven Rock and returns to the Citadel. \n \nWith the knowledge they possess, the G.E.C.K. and the means to activate Project Purity, the Brotherhood assault the Jefferson Memorial, spearheaded by a giant robot named Liberty Prime. In the control room of Project Purity the player confronts Colonel Autumn, and has the choice to persuade him to give up or kill him. Dr. Li informs the player that the purifier is ready to be activated, but the activation code must be input manually, and also that the control room is flooded with lethal amounts of radiation. The Lone Wanderer is forced to choose between sending Sarah Lyons of the Brotherhood inside the extremely irradiated purifier or entering themselves. Whoever enters into the chamber inputs the code hinted at through the game, that being 21:6, and dies from a radiation spike.'}, {'id': 9630, 'first_release_date': 1447113600, 'genres': [5, 12], 'involved_companies': [24120, 95327], 'name': 'Fallout 4'}, {'id': 131851, 'first_release_date': 1577750400, 'involved_companies': [94146, 94147], 'name': 'Fallout Shelter Online'}, {'id': 103020, 'first_release_date': 1542153600, 'genres': [5, 12], 'involved_companies': [65249, 95310], 'name': 'Fallout 76'}]
    genres_list = []

    for result in json_api_data:
        if "Collector's Edition" in result['name']:
            result.clear()
        if "Collection" in result['name']:
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
    print(json_api_data)
    return json_api_data







