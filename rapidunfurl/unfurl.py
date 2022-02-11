#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import functools

from micawber import Provider, ProviderRegistry, ProviderException

from .provider_data.noembed import NOEMBED_PROVIDER_LIST
from .provider_data.custom import CUSTOM_PROVIDER_LIST
from .provider_data.oembed import OEMBED_PROVIDER_LIST

__version__ = "1.0.0"
import micawber
import requests
from pyquery import PyQuery as pq
from uritools import urijoin


def get(url, timeout=5):
    try:
        x = None
        x = requests.get(url,
                         timeout=timeout,
                         headers={'User-Agent': 'RapidUnfurl/01.0'})
    except requests.exceptions.RequestException:
        x = None
    return x


def wrap_response(url, data):

    image = ("image" in data and data["image"]) or ""
    favicon = ("favicon" in data and data["favicon"]) or ""
    url = ("url" in data and data["url"]) or url

    if image:
        image = urijoin(url, image)

    if favicon:
        favicon = urijoin(url, favicon)

    return data


def updated_provider_list(list):
    if list == "OEMBED":
        providers = [
            [entry[0], entry[1].endpoint]
            for entry in micawber.bootstrap_basic()
        ]
        providers.extend(
            [[entry[0], entry[1].endpoint]
             for entry in micawber.bootstrap_oembed()]
        )
        return providers

    if list == "NOEMBED":
        return [[entry[0], entry[1].endpoint]
                for entry in micawber.bootstrap_noembed()]

    return []


def load_providers(provider_list="OEMBED", remote=False):
    provider = ProviderRegistry(None)

    if remote:
        providers = updated_provider_list(provider_list)
    else:
        providers = []
        if provider_list == "OEMBED":
            providers = OEMBED_PROVIDER_LIST
        if list == "NOEMBED":
            providers = NOEMBED_PROVIDER_LIST

    for entry in providers:
        provider.register(entry[0], Provider(entry[1]))

    return provider


def open_graph(html):

    d = pq(html)
    return {
        "type": d('meta[property="og:type"]').attr("content"),
        "url": d('meta[property="og:url"]').attr("content"),
        "title": d('meta[property="og:title"]').attr("content"),
        "site_name": d('meta[property="og:site_name"]').attr("content"),
        "description": d('meta[property="og:description"]').attr("content"),
        "image": d('meta[property="og:image"]').attr("content"),
        "audio": d('meta[property="og:audio"]').attr("content"),
        "locale": d('meta[property="og:locale"]').attr("content"),
        "video": d('meta[property="og:video"]').attr("content"),
    }


def twitter_card(html):

    d = pq(html)
    return {
        "card": d('meta[name="twitter:card"]').attr("content"),
        "url": d('meta[name="twitter:url"]').attr("content"),
        "site_name": d('meta[name="twitter:site"]').attr("content"),
        "creator": d('meta[name="twitter:creator"]').attr("content"),
        "description": d('meta[name="twitter:description"]').attr("content"),
        "image": d('meta[name="twitter:image"]').attr("content"),
        "title": d('meta[name="twitter:title"]').attr("content"),
    }


def meta_tags(html, favicon):

    d = pq(html)
    return {
        "title": d('meta[name="title"]').attr("content") or d("title").text(),
        "description": d('meta[name="description"]').attr("content"),
        "image": d('meta[name="image"]').attr("content"),
        "favicon": favicon,
        "url": d('meta[name="canonical"]').attr("content")
        or d('meta[name="url"]').attr("content"),
        "keywords": d('meta[name="keywords"]').attr("content"),
    }


def oembed(html, url, refresh_oembed_provider_list=False):
    try:
        embed = load_providers("OEMBED",
                               refresh_oembed_provider_list).request(url)
        if embed and "html" in embed:
            return embed
    except ProviderException:
        pass

    try:
        embed = load_providers("NOEMBED",
                               refresh_oembed_provider_list).request(url)
        if embed and "html" in embed:
            return embed
    except ProviderException:
        pass

    try:
        d = pq(html)
        oembed_url = d('link[type="application/json+oembed"]').attr("href")
        if oembed_url:
            return get(oembed_url).json()
    except requests.exceptions.RequestException:
        return None

    return None


def extend_dict(d1, d2):
    result = d2.copy()
    result.update({k: v for k, v in d1.items() if v})
    return result


def custom_unfurl(url, timeout=5):
    for regex, provider in CUSTOM_PROVIDER_LIST:
        if re.match(regex, url):
            return provider(url, timeout)
    return None


def get_favicon(html, url, timeout=5):

    d = pq(html)
    favicon = d('link[rel="icon"]').attr("href")
    if not favicon:
        favicon = d('link[rel="alternate icon"]').attr("href")
    if not favicon:
        favicon = d('link[rel="shortcut icon"]').attr("href")
    if not favicon:
        favicon_url = urijoin(url, "/favicon.ico")
        r = requests.head(favicon_url)
        if r.status_code == 200:
            favicon = favicon_url

    return favicon


def cleanNullTerms(data):
    clean = {}
    for k, _v in data.items():
        v = data.get(k)
        if isinstance(v, dict):
            nested = cleanNullTerms(v)
            if len(nested.keys()) > 0:
                clean[k] = nested
        elif bool(v):
            clean[k] = v
    return clean


@functools.lru_cache(maxsize=64)
def unfurl(url, timeout=5, refresh_oembed_provider_list=False):
    """
    :param url: The url to embed
    :param timeout: Timeout (in seconds) to allow url to load
    :param html: If you already have the html available you
                    can pass it in to save a network call
    :param refresh_oembed_provider_list: Set to True to
                    reload the provider list from oembed.com, otherwise
    the list that is included with pyunfurl is used
    :return: dict
    """
    data = {
        "url": url
    }

    r = get(url, timeout=timeout)

    if r is None:
        data = extend_dict(data, {"response": "unreachable"})
        return data
    elif not r.ok:
        data = extend_dict(data, {"response": str(r.status_code)})
        return data

    r_pq = pq(r.text)
    r_head = r_pq('head')

    favicon = get_favicon(r_head, url)

    data = custom_unfurl(url, timeout)
    if data:
        return wrap_response(url, data)

    data = oembed(r_head, url, refresh_oembed_provider_list)
    if data:
        return wrap_response(url, data)

    data = meta_tags(r_head, favicon)
    data = extend_dict(data, twitter_card(r_head))
    data = extend_dict(data, open_graph(r_head))
    data = extend_dict(data, {"url": url})
    clean_data = cleanNullTerms(data)
    return wrap_response(url, clean_data)
