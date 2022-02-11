# Changelog for RapidUnfurl

What changes have been made with different releases

## 1.0.0

- Changed how data was returned for unreachable URLs and for URLs with non-200 responses
- Ensured that the URL returned in the data is always the URL that was sent originally
- Set method definition of unfurl to by `async` so it can be better used by asyncio systems.
- Updated the makefile so that the clean operation cleans out the `__pycache__` directory
- Added a CHANGELOG.md

## 0.1.1

- First public release of RapidUnfurl
- Fix a ton of lynting and testing errors
  - fixed default spacing

## 0.1.0

- Updated the readme to reference unfurling from davintaddeo.com
- Fixed the example.py to use rapidunfurl instead of pyunfurl
- Added error handling to the get method that uses requests to retrieve data from URLs
- Put in a dict response to use after handling a failed URL data retrieval
- Implemented unit testing for rapidunfurl
- Updated setup.py authorship information
- Added functools.lru_cache to cache responses when the same URL is provided to the command

## 0.0.1

- First crack at differentiating rapidunfurl from pyunfurl
- Remove all the HTML code in the response
