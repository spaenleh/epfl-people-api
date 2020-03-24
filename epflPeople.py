import requests

SEARCH_URL = 'https://search.epfl.ch/json/ws_search.action'
PHOTO_URL = 'https://people.epfl.ch/private/common/photos/links/'


def __is_sciper(sciper):
    if isinstance(sciper, str):
        sciper = int(sciper)
    if not str(sciper).isnumeric() or sciper < 100000 or sciper > 999999:
        return False
    else:
        return True


def find_by_sciper(sciper, locale='en'):
    if not __is_sciper(sciper):
        raise TypeError
    payload = {'q': sciper, 'request_locale': locale}

    response = requests.get(SEARCH_URL, params=payload)

    '''
    ["accreds", "email", "firstname", "guest", "homePage", "name", "position", "profile", "sciper", "unit", "unitPath"]
    '''
    return response.json()[0]


def find(search, locale='en'):
    payload = {'q': search, 'request_locale': locale}

    response = requests.get(SEARCH_URL, params=payload)

    if response.status_code != requests.codes.ok:
        return None
    else:
        return response.json()[0]


def has_photo(sciper):
    if not __is_sciper(sciper):
        raise TypeError

    filename = str(sciper)+'.jpg'
    response = requests.get(PHOTO_URL+filename, stream=True)

    if response.status_code == requests.codes.ok:
        with open(filename, 'wb') as handle:
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
        return True
    else:  # 404
        return False
