#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import rapidunfurl

class UnitTests(unittest.TestCase):
  def test_import(self):
    self.assertIsNotNone(rapidunfurl)

  def test_custom_embed(self):
    custom = rapidunfurl.unfurl("https://news.ycombinator.com/item?id=16319505")
    self.assertEqual("https://news.ycombinator.com/favicon.ico", custom["favicon"], "custom:favicon")
    self.assertEqual("https://news.ycombinator.com/item?id=16319505", custom["url"], "custom:url")
    self.assertEqual("SpaceX’s Falcon Heavy successfully launches", custom["title"], "custom:title")
    self.assertEqual("", custom["description"], "custom:description")

    custom = rapidunfurl.unfurl("https://news.ycombinator.com/item?id=16319522")
    self.assertEqual("https://news.ycombinator.com/favicon.ico", custom["favicon"], "custom:favicon")
    self.assertEqual("https://news.ycombinator.com/item?id=16319522", custom["url"], "custom:url")
    self.assertEqual("SpaceX’s Falcon Heavy successfully launches", custom["title"], "custom:title")
    self.assertEqual("There was something doubly awesome about the two falcons landing at the same time right next to each other!", custom["description"], "custom:description")

  def test_oembed(self):
    oembed = rapidunfurl.unfurl("https://www.youtube.com/watch?v=v-eK_cpTsOw")
    self.assertEqual("https://www.youtube.com/", oembed["provider_url"], "oembed:provider_url")
    self.assertEqual("https://www.youtube.com/watch?v=v-eK_cpTsOw", oembed["url"], "oembed:url")
    self.assertEqual("Adam Savage Answers: What's the Scariest Experience You've Had on Mythbusters?", oembed["title"], "oembed:title")
    self.assertEqual("YouTube", oembed["provider_name"], "oembed:provider_name")
    self.assertEqual("video", oembed["type"], "oembed:type")
    self.assertEqual("https://i.ytimg.com/vi/v-eK_cpTsOw/hqdefault.jpg", oembed["thumbnail_url"], "oembed:thumbnail_url")
    self.assertEqual(113, oembed["height"], "oembed:height")
    self.assertEqual("Adam Savage’s Tested", oembed["author_name"], "oembed:author_name")

  def test_open_graph(self):
    og = rapidunfurl.unfurl("https://www.imdb.com/title/tt0117500/?q=none")
    self.assertEqual("https://m.media-amazon.com/images/M/MV5BZDJjOTE0N2EtMmRlZS00NzU0LWE0ZWQtM2Q3MWMxNjcwZjBhXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_FMjpg_UX1000_.jpg", og["image"], "og:image")
    self.assertEqual("https://www.imdb.com/title/tt0117500/", og["url"], "og:url")
    self.assertEqual("The Rock (1996) - IMDb", og["title"], "og:title")
    self.assertEqual("IMDb", og["site_name"], "og:site_name")
    self.assertEqual("video.movie", og["type"], "og:type")
    self.assertRegex(og["description"], "Directed by Michael Bay. With Sean Connery, Nicolas Cage, Ed Harris, John Spencer")

  def test_twitter_card(self):
    card = rapidunfurl.unfurl("https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup")
    self.assertEqual("https://cdn.cms-twdigitalassets.com/content/dam/developer-twitter/redesign-2021-images/og-social-card/devwebsite_card_tn.jpg.twimg.768.jpg", card["image"], "card:image")
    self.assertEqual("https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup", card["url"], "card:url")
    self.assertEqual("Cards markup | Docs | Twitter Developer Platform", card["title"], "card:title")
