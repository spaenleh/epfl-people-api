import sys
import epflpeople


def main(search_term):
    if search_term:
        print(epflpeople.find(search_term))


if __name__ == '__main__':
    print(sys.argv)
    main(sys.argv)
