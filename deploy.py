import subprocess
from subprocess import PIPE, STDOUT
import sys, os
from pathlib import Path
import re

DEFAULT_ARG = 'test'
ARGS = {
    DEFAULT_ARG: 'https://test.pypi.org/legacy/',
    'release': 'https://upload.pypi.org/legacy/',
}

DIST_FOLDER = Path('dist')
LATEST = 'latest'

RE_VERSION_NUMBER = r"^\w*-([\da-z]+.[\da-z]+.[\da-z]+)"


def main(mode):
    create_dist_dir()
    print(f'deploying as {mode}')
    res = subprocess.check_output(f"find {os.getcwd()} -iname VERSION -not -path build".split(), encoding='utf-8').splitlines()
    version_path = res[0].strip()
    version = Path(version_path).read_text().strip()

    # rotating the versions
    latest_dir = (DIST_FOLDER / LATEST)
    if latest_dir.exists():
        # get version name
        previous_version = get_previous_version(latest_dir)
        if version in previous_version:
            warn_same_version(previous_version, version)
            re_upload = validate_prompt(f'try re-uploading {version} ?')
            if re_upload:
                upload(mode, previous_version)
            print('exiting')
            exit()
        else:
            # rename old version to its name
            try:
                latest_dir.rename(DIST_FOLDER / previous_version)
            except OSError:
                print(f'Version in {LATEST} folder ({previous_version}) already has a folder')
                latest_dir.rename(DIST_FOLDER / (previous_version + '_duplicate'))

    previous_version = get_previous_version()
    if previous_version:
        while previous_version:
            print(f'detected previous version : {previous_version}')
            new_dir_name = previous_version
            if version in previous_version:
                new_dir_name = LATEST
                warn_same_version(previous_version, version)
            # move previous version in a dedicated folder
            move_files(previous_version, new_dir_name)
            # re-run until there are no more previous versions
            previous_version = get_previous_version()
    else:
        print(f'no previous version found in {DIST_FOLDER}')

    # build the distribution
    print(f'building version {version}')
    print(subprocess.check_output(f"python setup.py sdist -d {latest_dir} bdist_wheel -d {latest_dir}".split(),
                                  encoding='utf-8'))

    # upload
    upload(mode, version)


def warn_same_version(previous_version, version):
    print(f'[SAME VERSION Error] VERSION specifies {version} and latest is {previous_version}')


def upload(mode, version):
    """
    Upload files that are in the 'latest' dir to the chosen repo

    :param version: version of the package
    :param mode: type of deploy
    """
    print(f'uploading version {version}')
    upload_command = f"twine upload --repository-url {ARGS[mode]} {(DIST_FOLDER / LATEST)}/*".split()
    subprocess.run(upload_command, encoding='utf-8')


def create_dist_dir():
    if not DIST_FOLDER.exists():
        print(f'creating {DIST_FOLDER} folder')
        DIST_FOLDER.mkdir(parents=True)


def move_files(version, new_dir_name=None):
    if not new_dir_name:
        new_dir_name = version
    files_to_move = get_files(version)
    dest_dir = (DIST_FOLDER / new_dir_name)
    dest_dir.mkdir()
    [file.rename(dest_dir / file.name) for file in files_to_move]


def get_files(pattern):
    return [file_name for file_name in DIST_FOLDER.iterdir() if pattern in file_name.name and file_name.is_file()]


def get_previous_version(folder=DIST_FOLDER):
    versions = []
    for file_name in folder.iterdir():
        res = re.match(RE_VERSION_NUMBER, str(file_name.name))
        if res:
            versions.append(res.groups()[0])
    versions = sorted(list(set(versions)))
    return versions[-1] if len(versions) > 0 else None


def find_version():
    for root, dirs, files in os.walk(Path(__file__).parent):
        for name in files:
            print(name)


def print_help():
    print('this script takes a single argument :')
    max_length_key = max([len(k) for k in ARGS.keys()])
    for arg_value, arg_url in ARGS.items():
        print(f'\t{arg_value.ljust(max_length_key)} : upload to {arg_url}')


def validate_prompt(message):
    res = input(message + ' (y/n): ')
    return res.lower() in ['y', '', 'yes']


if __name__ == '__main__':
    mode = DEFAULT_ARG
    # handle command line
    try:
        mode = sys.argv[1]
        if mode not in ['test', 'release']:
            print_help()
            exit()

    except IndexError:
        print_help()
        use_test = validate_prompt('Use mode=\'test\' ?')
        if use_test:
            print('setting mode to \'test\'')
        else:
            print('exiting')
            exit()
    main(mode)
