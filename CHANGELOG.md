# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Created `clean_data.py` script to clean and reformat CSV data.
- Added error handling and logging to `clean_data.py`.
- Added parsing and splitting of `model` and `engine` columns in `clean_data.py`.

### Changed
- Updated `clean_data.py` to handle cases where `engine` column has unexpected formats.
- Ensured all values are converted to strings before processing in `clean_data.py`.

### Fixed
- Fixed "list index out of range" error in `clean_data.py`.
- Fixed "argument of type 'float' is not iterable" error in `clean_data.py`.

## [Initial Release]
- Initial setup of the repository.
