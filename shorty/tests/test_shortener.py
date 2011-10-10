# -*- coding: utf-8 -*-
#    This file is part of Shorty.
#
#    Shorty is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Shorty is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Shorty.  If not, see <http://www.gnu.org/licenses/>.

from unittest import main, TestCase

from shorty.core.shortener import UrlEncoder

TEST_DATA = {
    7       : '9kexw',
    21      : 'p3zuu',
    35      : 'g3cbs',
    126     : 'vfcs2',
    196     : '6wquv',
    181892  : '6pgke',
    181929  : 'b7h7r',
    181966  : 'vcxfn',
    183150  : 'vgyp2',
    183187  : 'w8q79',
    183224  : '6j7fy',
    185185  : '8z5pj',
    185222  : '4f2ja',
    185259  : '9c8x4',
    199874  : '2ex63',
    199911  : '5y7c9',
    199948  : 'jwjwa',
    199985  : '8q9ws',
}


class EncodeDecodeTestCase(TestCase):
    def setUp(self):
        self.encoder = UrlEncoder()

    def test_encoding(self):
        for decoded, expected in TEST_DATA.iteritems():
            encoded = self.encoder.encode_id(decoded)
            self.assertEqual(encoded, expected,
                             msg="Encoder returned '%s' for id %d (expected '%s')" % (
                                 encoded, decoded, expected))

    def test_decoding(self):
        for expected, encoded in TEST_DATA.iteritems():
            decoded = self.encoder.decode_id(encoded)
            self.assertEqual(decoded, expected,
                             msg="Decoder returned %d for code '%s' (expected %d)" % (
                                 decoded, encoded, expected))


if __name__ == '__main__':
    main()
