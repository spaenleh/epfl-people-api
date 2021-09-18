import requests

SEARCH_URL = 'https://search.epfl.ch/json/ws_search.action'
PHOTO_URL = 'https://people.epfl.ch/private/common/photos/links/'


def find_by_sciper(sciper, locale='en'):
    """
    Find a person's info from the given sciper
    :param sciper: Sciper number of the person
    :param locale: response in english ('en') or in french ('fr')
    :return: Person info if the person is found else an error string explaining the problem
    """
    if not __is_sciper(sciper):
        return 'Expected sciper number but found ' + repr(sciper)
    payload = {'q': sciper, 'request_locale': locale}

    response = requests.get(SEARCH_URL, params=payload)
    '''
    ["accreds", "email", "firstname", "guest", "homePage", "name", "position", "profile", "sciper", "unit", "unitPath"]
    '''
    if response.status_code == requests.codes.ok:
        if len(response.text) > 2:
            return response.json()
        else:
            return 'This person does not exist'
    else:
        return 'External service not responding'


def find(search, locale='en'):
    """
    Find a person using any general criteria (email, sciper, name, surname, etc ...)
    :param search: a string to search a person
    :param locale: response in english ('en') or in french ('fr')
    :return: Person info if the person is found else an error string explaining the problem
    """
    payload = {'q': search, 'request_locale': locale}

    response = requests.get(SEARCH_URL, params=payload)

    if response.status_code == requests.codes.ok:
        if len(response.text) > 2:
            return response.json()
        else:
            return 'This person does not exist'
    else:
        return 'External service not responding'


def has_photo(sciper):
    """
    Search if a person has a public photo
    :param sciper: sciper from person
    :return: Photo url if found else None
    """
    url = PHOTO_URL + str(sciper) + '.jpg'
    response = requests.get(url, stream=True)

    if response.status_code == requests.codes.ok:
        return url
    else:  # 404
        return None


def __is_sciper(sciper):
    """
    Checks if the given argument is a valid Sciper number
    :param sciper: sciper to check
    :return: Whether sciper is valid or not
    """
    if str(sciper).isnumeric():
        sciper = int(sciper)
        if 100000 < sciper < 999999:
            return True
    return False
