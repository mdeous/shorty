# -*- coding: utf-8 -*-

from sqlalchemy.orm.exc import NoResultFound

from shorty import db
from shorty.models import ShortURL


class EncoderError(Exception):
    """
    Exception for errors that occur while encoding/decoding
    a short URL.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class UrlEncoder(object):
    """
    Short URL Generator
    ===================

    Python implementation for generating Tiny URL- and bit.ly-like URLs.

    A bit-shuffling approach is used to avoid generating consecutive, predictable
    URLs.  However, the algorithm is deterministic and will guarantee that no
    collisions will occur.

    The URL alphabet is fully customizable and may contain any number of
    characters.  By default, digits and lower-case letters are used, with
    some removed to avoid confusion between characters like o, O and 0.  The
    default alphabet is shuffled and has a prime number of characters to further
    improve the results of the algorithm.

    The block size specifies how many bits will be shuffled.  The lower BLOCK_SIZE
    bits are reversed.  Any bits higher than BLOCK_SIZE will remain as is.
    BLOCK_SIZE of 0 will leave all bits unaffected and the algorithm will simply
    be converting your integer to a different base.

    The intended use is that incrementing, consecutive integers will be used as
    keys to generate the short URLs.  For example, when creating a new URL, the
    unique integer ID assigned by a database could be used to generate the URL
    by using this module.  Or a simple counter may be used.  As long as the same
    integer is not used twice, the same short URL will not be generated twice.

    The module supports both encoding and decoding of URLs. The min_length
    parameter allows you to pad the URL if you want it to be a specific length.

    Sample Usage:

    >>> import short_url
    >>> url = short_url.encode_url(12)
    >>> print url
    LhKA
    >>> key = short_url.decode_url(url)
    >>> print key
    12

    Use the functions in the top-level of the module to use the default encoder.
    Otherwise, you may create your own UrlEncoder object and use its encode_url
    and decode_url methods.

    Author: Michael Fogleman
    License: MIT
    Link: http://code.activestate.com/recipes/576918/

    Minor changes by Mathieu D. <mattoufootu[at]gmail.com>
    """
    alphabet = 'mn6j2c4rv8bpygw95z7hsdaetxuk3fq'
    block_size = 24
    min_length = 5
    mask = (1 << block_size) - 1
    mapping = list(reversed(range(block_size)))

    def encode_id(self, id):
        """
        Encodes an integer.

        :param id: The integer to encode.
        :type id: int.
        :returns: str -- the encoded value.
        """
        return self.enbase(self.encode(id))

    def encode(self, n):
        return (n & ~self.mask) | self._encode(n & self.mask)
    def _encode(self, n):
        result = 0
        for i, b in enumerate(self.mapping):
            if n & (1 << i):
                result |= (1 << b)
        return result

    def enbase(self, x):
        result = self._enbase(x)
        padding = self.alphabet[0] * (self.min_length - len(result))
        return '%s%s' % (padding, result)
    def _enbase(self, x):
        n = len(self.alphabet)
        if x < n:
            return self.alphabet[x]
        return self._enbase(x / n) + self.alphabet[x % n]

    def decode_id(self, encoded):
        """
        Decodes a value encoded with :func:`UrlEncoder.encode_id`.

        :param encoded: The value to decode.
        :type encoded: str.
        :returns: int -- the decoded value.
        """
        return self.decode(self.debase(encoded))

    def decode(self, n):
        return (n & ~self.mask) | self._decode(n & self.mask)
    def _decode(self, n):
        result = 0
        for i, b in enumerate(self.mapping):
            if n & (1 << b):
                result |= (1 << i)
        return result

    def debase(self, x):
        n = len(self.alphabet)
        result = 0
        for i, c in enumerate(reversed(x)):
            try:
                result += self.alphabet.index(c) * (n ** i)
            except ValueError:
                raise EncoderError("Encoded value characters don't match the "
                                   "defined alphabet.")
        return result


def shorten_url(url, slug=''):
    """
    Adds a long URL to the database and returns its encoded id.

    :param url: The URL to shorten.
    :type url: str.
    :returns: str -- the short URL code (only the code, not the full URL)
    """
    try:
        url_obj = ShortURL.query.filter_by(long_url=url).one()
    except NoResultFound:
        url_obj = ShortURL(long_url=url)
        if slug:
            url_obj.slug = slug
        db.session.add(url_obj)
        db.session.commit()
    if url_obj.slug:
        return url_obj.slug
    else:
        encoded = UrlEncoder().encode_id(url_obj.id)
        return encoded

def expand_url(url):
    """
    Expands a short URL.

    :param url: The short URL to expand.
    :type url: str.
    :returns: str -- the corresponding long URL.
    """
    url_code = url.split('/')[-1] if ('/' in url) else url
    url_id = UrlEncoder().decode_id(url_code)
    url_obj = ShortURL.query.filter_by(id=url_id).one()
    return url_obj.long_url


def expand_slug(slug):
    """
    Expands a slug.

    :param slug: The slug to expand.
    :type url: str.
    :returns: str -- the corresponding long URL.
    """
    url_code = slug.split('/')[-1] if ('/' in slug) else slug
    url_obj = ShortURL.query.filter_by(slug=slug.lower()).one()
    return url_obj.long_url
