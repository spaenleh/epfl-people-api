import re
import requests
from .errors import *

SEARCH_URL = 'https://search.epfl.ch/json/ws_search.action'
PHOTO_URL = 'https://people.epfl.ch/private/common/photos/links/'

PP_PRINT = [
    'firstname',
    'name',
    'position',
    'unit',
    'sciper',
    'email',
    'homepage',
    'guest',
    'unitPath',
]
ACCREDS = 'accreds'
PP_PRINT_ACCREDS = [
    'acronym',
    'name',
    'position',
    'office',
    'status',
    'homepage',
    'address',
    'phones',
    'officeList',
    'phoneList',
]

COLOR_RESET = '\033[m'
RED = '\033[31m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
GRAY = '\033[37m'
GREEN = '\033[32m'


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
            raise NoResultError
    else:
        raise ServiceNotResponding


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
        if len(response.text) > 2:  # not an empty array
            return response.json()
        else:
            raise NoResultError(search)
    else:
        raise ServiceNotResponding


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


def find_first(search, format_output=False, **kwargs):
    try:
        res = find(search, **kwargs)[0]
    except (NoResultError, ServiceNotResponding) as e:
        return str(e)
    except ConnectionError:
        return h('No connection, please check that you are connected', YELLOW)
    if format_output:
        return pretty_print(res, search=search, **kwargs)
    else:
        return res


def find_all(search, format_output=True, **kwargs):
    try:
        res = find(search, *kwargs)
    except (NoResultError, ServiceNotResponding) as e:
        return h(str(e), **kwargs)
    except requests.exceptions.ConnectionError as e:
        return h('No connection, please check that you are connected', YELLOW, **kwargs)
    if format_output:
        output = ''
        for i, r in enumerate(res):
            output += h(f'\n\n===== Result {i} =====\n', BLUE, **kwargs)
            output += pretty_print(r, search=search, **kwargs)
        return output
    else:
        return res


def pretty_print(people: dict, **kwargs):
    output = h('\n--- General info ---\n', GREEN, **kwargs)
    output += '\n'.join(enumerate_properties(people, PP_PRINT, **kwargs)) + '\n'
    for i, accred in enumerate(people.get(ACCREDS)):
        output += h(f'\n--- Accred {i+1} ---\n', GREEN, **kwargs)
        output += '\n'.join(enumerate_properties(accred, PP_PRINT_ACCREDS, **kwargs)) + '\n'
    return output


def enumerate_properties(obj, key_list, search, highlight=False):
    max_w = max([len(k) for k in key_list])
    for key in key_list:
        value = obj.get(key)
        if value:
            if isinstance(value, list):
                yield f'{key.capitalize().ljust(max_w)}: {", ".join(value)}'
                return
            if key == 'address':
                value = value.replace('$', '\n'+' '*(max_w+1))
            if highlight:
                value = highlight_text(value, search)
                for term in search.split():
                    value = value.replace(term, h(term, RED))
            yield f'{key.capitalize().ljust(max_w)}: {value}'


def highlight_text(value, search):
    for term in search.split():
        matches = re.findall(term, value, re.I)
        for match in matches:
            value = value.replace(match, h(match, RED))
    return value


def h(text, color=RED, highlight=True, **kwargs):
    if highlight:
        return f'{color}{text}{COLOR_RESET}'
    else:
        return text
