import sys
from . import epflpeople


def main():
    print('Running EPFL People without highlighting')
    search_term = input('Find : ')
    if search_term:
        print(epflpeople.find_all(search_term, format_output=True, highlight=False))


def main_highlighted():
    print('Running EPFL People with highlighting')
    search_term = input('Find : ')
    if search_term:
        print(epflpeople.find_all(search_term, format_output=True, highlight=True))


if __name__ == '__main__':
    main_highlighted()
