# flet-m3-carousel

![Demo](https://raw.githubusercontent.com/programmersd21/flet-m3-carousel/main/assets/demo.gif)


A Flet extension that wraps the Flutter `m3_carousel` package and exposes it as
the `M3Carousel` layout control.

The carousel layout and animation are delegated to the upstream package. This
wrapper does not reimplement them.

## Platform support

Tested on Linux desktop. Other platforms are supported by the upstream package
but were not tested here.

| Platform | Status |
|---|---|
| Linux | Tested |
| Windows | Not tested |
| macOS | Not tested |
| Web | Not tested |
| iOS | Not tested |
| Android | Not tested |

## Installation

Install the Python package:

```bash
pip install flet-m3-carousel
```

The Flutter side is built into the Flet client. After changing Dart code, rebuild
the client.

## Quick start

```python
import flet as ft
from flet_m3_carousel import M3Carousel, M3CarouselItem


def main(page: ft.Page):
    page.add(
        M3Carousel(
            height=320,
            layout="hero",
            axis="horizontal",
            hero_alignment="center",
            items=[
                M3CarouselItem(key="mountains", image="assets/mountains.jpg", title="Mountains"),
                M3CarouselItem(key="city", image="assets/city.jpg", title="City"),
                M3CarouselItem(key="ocean", image="assets/ocean.jpg", title="Ocean"),
            ],
            on_tap=lambda e: print(e.index, e.item_key),
        )
    )


ft.run(main)
```

## Layouts

| Value | Upstream type | Description |
|---|---|---|
| `hero` | `M3CarouselType.hero` | One large item with small peeking neighbors. |
| `contained` | `M3CarouselType.contained` | Items stay contained in the content area. |
| `uncontained` | `M3CarouselType.uncontained` | Items scroll to the container edge. |
| `uncontainedMultiAspect` | `M3CarouselType.uncontainedMultiAspect` | Uncontained items with their own widths. |
| `fullScreen` | `M3CarouselType.fullScreen` | One edge to edge item, scrolled vertically. |

## Events

- `on_tap`: fires when an item is tapped. Payload has `index` (zero based) and
  `item_key`.
- `on_change`: fires when the focal item changes after scrolling. Payload has
  `index` and `item_key`.

## Demo

A runnable example is in `examples/flet_m3_carousel_example`. Build and run it with:

```bash
cd examples/flet_m3_carousel_example
flet build linux
flet run
```

## Compatibility

This package follows Flet's extension model. Build the client after changing
Dart code. Python-only changes do not require a rebuild.

## Known limitations

- Item content is image-based. Arbitrary Flet controls are not supported as
  item content.
- Autoplay, infinite looping, custom physics, and custom spring curves are not
  exposed by the upstream package.
- Asset images must be declared in the app `pubspec.yaml`. A Python relative
  path is not a Flutter asset path.

## License

MIT for this wrapper. The upstream package is also MIT licensed.
