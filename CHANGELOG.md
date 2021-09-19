# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added

### Changed

### Removed


## [0.0.4] - 2021-09-17
### Added
- Coloring of the output
- New utility called `epflpeople_pretty` that displays the search output with colors
- Added a MANIFEST.in to ensure that the VERSION file is packaged
- Added new error classes to deal with different scenarios
- Added some information and an input field to make a search on the cli

### Changed
- Changed how version is found in deploy.py
- Changed long_description to include CHANGELOG on PyPI
- Updated project urls to point to useful places (GitHub, Documentation, CHANGELOG)

### Removed
- Removed command line arguments in \_\_main\_\_.py as they are not supported

## [0.0.1] - 2021-09-19
### Added
- Added deploy.py script to aid deploying on PyPI
- Added shebang at beginning of setup.py to enable running on cli

### Changed
- Changed project url to point to the [github repository][REPO]
- Changed LICENSE to be consistent, now using MIT


## [0.0.0] - 2021-09-19
### Added
- Added epflpeople package
- Added setup.py script
- Configured repo and project
- Added a LICENSE
- Added base information in README.md



[Unreleased]: https://github.com/spaenleh/epfl-people-api/compare/v0.0.4...HEAD
[0.0.4]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.1...v0.0.3
[0.0.1]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.0...v0.0.1
[0.0.0]: https://github.com/spaenleh/epfl-people-api/releases/tag/v0.0.0

[REPO]: https://github.com/spaenleh/epfl-people-api


