# Events

## on_tap

Fires when an item is tapped. Payload:

- `index`: zero based item index.
- `item_key`: the item key, or None.

## on_change

Fires when the focal item changes after scrolling. Payload:

- `index`: zero based focal item index.
- `item_key`: the item key, or None.

It does not fire on scroll position. No per pixel updates are sent to Python.
