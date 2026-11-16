# Card fonts

These fonts are used by `scripts/generate_cards.py` to build the 16:9 cards in `assets/img/cards/`.

| File | Used for | License |
| --- | --- | --- |
| `Borel-Regular.ttf` | command tokens | SIL OFL 1.1, see `licenses/OFL-Borel.txt` |
| `Chilanka-Regular.ttf` | notes | SIL OFL 1.1, see `licenses/OFL-Chilanka.txt` |
| `LondrinaSolid-Regular.ttf` | card title | SIL OFL 1.1, see `licenses/OFL-LondrinaSolid.txt` |
| `ShadowsIntoLightTwo-Regular.ttf` | pretitle, subtitle, number, signature | SIL OFL 1.1, see `licenses/OFL-ShadowsIntoLightTwo.txt` |

Borel and Chilanka are the same files that are embedded in `assets/css/embedded-fonts.css`.
Londrina Solid and Shadows Into Light Two are the Latin subsets published by Google Fonts
(via the `@fontsource` npm packages), unpacked from WOFF to TTF.

Mermaid measures text while it lays out a diagram, so Borel and Chilanka have to be installed
on the machine that generates the cards. Run this once:

```bash
python3 scripts/generate_cards.py --install-fonts
```
