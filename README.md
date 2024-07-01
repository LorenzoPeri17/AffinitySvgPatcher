# AffinitySvgPatcher

Patches Matplotlib-generated svg to be able to open them properly in Affinity Designer.

## Usage

``` python
from AffinitySvgPatcher import AffinitySvgPatcher

patcher = AffinitySvgPatcher('path/to/file.svg')
patcher.patch_svg(save = True, save_dir = 'dir/to/save', postfix = '-patched')
```

## Patches

For now I have discovered the following tricks:

* in `text` elements, replace `font` attributes with `font-size` and `font-family` (`font` is [apparently ignored](https://forum.affinity.serif.com/index.php?/topic/173734-font-sizes-in-imported-svg-documents-are-sometimes-interpreted-incorrectly/) by AD),
* in `xlink:href` (which are [deprecated](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/xlink:href)) replace `x` and `y` attributes with `transform=translate(x y)` (AD seems to ignore `x` or `y` attributes).

If more issues become known, PRs or GH issues are welcome! :)
