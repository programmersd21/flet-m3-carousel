# Troubleshooting

- SDK too old: m3_carousel 2.1.5 requires Dart >= 3.13.0 and
  Flutter >= 3.47.0. Flet 1.0.5 requires Flutter 3.44.8. These do not overlap.
- Missing assets: declare image assets in the app `pubspec.yaml`.
- Stale build after a Flutter change: rebuild the client.
- Unsupported platform: only Linux was tested.
