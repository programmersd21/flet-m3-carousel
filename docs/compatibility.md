# Compatibility

Verified versions:

- Flet: 1.0.5
- Flutter: 3.47.7 (via flutterup) for building. Flet 1.0.5 itself requires
  Flutter 3.44.8, which is incompatible with m3_carousel 2.1.5.
- Dart: 3.13.5
- m3_carousel: 2.1.5 (requires Dart >= 3.13.0, Flutter >= 3.47.0)

Commands used:

- `flet --version`
- `flutter --version`
- `dart --version`
- `flutter analyze`
- `flutter test`
- `ruff check`
- `ruff format --check`
- `pytest`

The newer m3_carousel 2.1.5 API is used because it provides `M3CarouselItem`
with image, title, and subtitle. Versions 2.1.4 and older use a different API.
