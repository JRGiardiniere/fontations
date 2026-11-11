#!/usr/bin/env python3
"""Generates the malformed test fonts that check skera degrades like hb-subset.

* post-malformed-glyph-names.ttf: a post format 2 table with zero-length glyph names, a name
  index past the end of the string data, and a glyphNameIndex shorter than the glyph count.

Usage, from the skera directory:
    test-data/generate-malformed-fonts.py
"""

import os
import struct

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables.DefaultTable import DefaultTable

FONTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
GLYPHS = [".notdef", "space", "A", "B", "C", "D", "acutecomb"]
CMAP = {0x20: "space", 0x41: "A", 0x42: "B", 0x43: "C", 0x44: "D", 0x301: "acutecomb"}


def box():
    pen = TTGlyphPen(None)
    pen.moveTo((100, 0))
    pen.lineTo((100, 700))
    pen.lineTo((500, 700))
    pen.lineTo((500, 0))
    pen.closePath()
    return pen.glyph()


def build_font(family):
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(GLYPHS)
    fb.setupCharacterMap(CMAP)
    glyphs = {name: box() for name in GLYPHS}
    glyphs["space"] = TTGlyphPen(None).glyph()
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics({name: (600, 0 if name == "space" else 100) for name in GLYPHS})
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupNameTable({"familyName": family, "styleName": "Regular"})
    fb.setupOS2()
    fb.setupPost()
    # fixed timestamps, so the fonts are reproducible
    fb.font["head"].created = fb.font["head"].modified = 0
    fb.font.recalcTimestamp = False
    return fb.font


def raw_table(tag, data):
    table = DefaultTable(tag)
    table.data = data
    return table


def post_malformed_glyph_names():
    font = build_font("Post Malformed Glyph Names")
    # version 2.0, italicAngle 0, underlinePosition -100, underlineThickness 50, the rest 0
    header = struct.pack(">Iihh5I", 0x00020000, 0, -100, 50, 0, 0, 0, 0, 0)
    # A and B name empty strings, C a real name, D an index past the string data; the
    # glyphNameIndex covers 6 of the 7 glyphs, so acutecomb has no entry.
    indices = [0, 3, 258, 259, 260, 300]
    names = [b"", b"", b"C.alt"]
    data = header + struct.pack(">H%dH" % len(indices), len(indices), *indices)
    data += b"".join(bytes([len(name)]) + name for name in names)
    font["post"] = raw_table("post", data)
    return font


def main():
    for name, build in (
        ("post-malformed-glyph-names.ttf", post_malformed_glyph_names),
    ):
        path = os.path.join(FONTS_DIR, name)
        build().save(path)
        print("wrote", path)


if __name__ == "__main__":
    main()
