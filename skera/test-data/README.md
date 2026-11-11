# test files

This directory contains files used for testing.


## test font sources
Describes the provenance, usage and generation procedures for font data used for testing.

  * source: https://github.com/harfbuzz/harfbuzz/tree/main/test/subset/data/fonts
  * source license file: https://github.com/harfbuzz/harfbuzz/blob/main/test/COPYING
  * license: [Open Font License][OFL]
  * usage: subsetter testing
    ```shell
    cargo run -- --path=font-file --text=abc --output-file=subset.ttf
    ```

[OFL]: https://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=OFL

## malformed test fonts
`fonts/post-malformed-glyph-names.ttf` and `fonts/gdef-invalid-mark-attach-class-def.ttf` are
synthetic fonts written with fontTools by `generate-malformed-fonts.py`. They check that skera
copes with malformed tables the way hb-subset does.
