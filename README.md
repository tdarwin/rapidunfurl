# RapidUnfurl

RapidUnfurl is a Python library designed to pull and process metadata very quickly to unfurl URL contents into a JSON object that can the be used by other programs for portraying that data, similar to how link expansion works in apps like Slack.

This library was originally forked from Loftie Ellis' [pyunfurl](https://github.com/lpellis/pyunfurl) library, which is an awesome project.  I just wanted to do some things to speed up the process, and drop away the html rendering, which I didn't need.

## Features

* Supports all oEmbed providers from [https://oembed.com/](https://oembed.com/) and [https://noembed.com/](https://noembed.com/) by default.
* Supports the [autodiscovery](https://oembed.com/#section4) part of the oEmbed spec.
* Support for [Open Graph](https://ogp.me/) protocol.
* Support for [Twitter Cards](https://developer.twitter.com/en/docs/tweets/optimize-with-cards/overview/abouts-cards.html)
* Falls back to Meta tags and the site favicon/title if all else fails.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pyunfurl.

```bash
pip install rapidunfurl
```

## Usage

```python
import rapidunfurl
rapidunfurl.unfurl('https://www.youtube.com/watch?v=aBr2kKAHN6M') 
```

This will return a dict similar to the oembed spec:

```json
{
  'method': 'oembed', # one of 'oembed', 'twitter_card', 'open_graph', 'meta_tags', 'custom'
  'site': 'YouTube', 
  'domain': 'youtube.com', 
  'title': 'Live Views of Starman', 
  'description': '', 
  'image': '', 
  'favicon': '',  # only included if no image was found 
  'url': 'https://www.youtube.com/watch?v=aBr2kKAHN6M', 
  'type': 'rich'
}
```

## Contributing

Pull requests are welcome. RapidUnfurl supports some custom integrations for sites that doesnt return any meta tags, if you want to improve the integration for a specific site you can look at the hackernews example.

## License

[MIT](https://choosealicense.com/licenses/mit/)
