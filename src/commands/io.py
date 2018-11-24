import requests

def loadio(realm,name):
        realm = realm.replace("'", '').replace('_', ' ').lower().encode('utf-8')
        name = name
        realms = []
        races = {
                1: 'A:Human', 2: 'H:Orc', 3:'A:Dwarf', 4:'A:Night Elf',
                5: 'H:Undead', 6: 'H:Tauren', 7:'A:Gnome', 8:'H:Troll',
                9: 'H:Goblin', 10: 'H:Blood Elf', 11: 'A:Draenei', 24:'A:Pandaren',
                22: 'A:Worgen', 25: 'A:Pandaren', 26: 'H:Pandaren'
        }

        classes = {
                1: 'Warrior', 2: 'Paladin', 3: 'Hunter', 4: 'Rogue',
                5: 'Priest', 6:'Death Knight', 7: 'Shaman', 8: 'Mage',
                9: 'Warlock', 10: 'Monk', 11: 'Druid'
        }


        try:
                realmlist = requests.get('https://us.api.battle.net/wow/realm/status?apikey=xxxxxxxxx').json()

                for realm_object in realmlist['realms']:
                        realms.append(realm_object['name'].lower().replace("'", '').encode('utf8'))
                if realm not in realms:
                        return 'Invalid realm. (instead of using spaces in a realm name, use an underscore, ex Aerie_Peak) (%s)' % realm
        except:
                return 'Error connecting to Battle.net API.'



        try:
                realm = realm.decode('utf-8')
                iorealm = realm.replace(" ", '-')

                character_object = requests.get('https://raider.io/api/v1/characters/profile?region=us&realm=%s&name=%s&fields=gear,mythic_plus_scores' % (iorealm, name)).json()
                try:
                        return character_object['reason']
                except KeyError:
                        try:
                                name = name.title()
                                ioscore = character_object['mythic_plus_scores']['all']
                                race = character_object['race']
                                class_ = character_object['class']
                                resp = 'Name:%s IOScore:%s Class:%s Race:%s' % (
                                        name, ioscore, class_, race
                                )

                                return resp
                        except:
                                return 'Error: Could not find Toon!'

        except:
                return 'Error connecting to the Battle.net API.'
