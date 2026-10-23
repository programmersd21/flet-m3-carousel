# API

## M3Carousel

Additional fields include `autoplay` (bool, default False) and `autoplay_interval` (int, default 3000).

Inherits from `flet.LayoutControl`.

- `items`: list of `M3CarouselItem`. Default empty list.
- `layout`: one of `hero`, `contained`, `uncontained`,
  `uncontainedMultiAspect`, `fullScreen`. Default `hero`.
- `axis`: `horizontal` or `vertical`. Default `horizontal`.
- `hero_alignment`: `left`, `center`, or `right`. Default `center`.
- `on_tap`: event handler. Payload fields `index` and `item_key`.
- `on_change`: event handler. Payload fields `index` and `item_key`.

## M3CarouselItem

- `image`: non empty string. Required.
- `key`: stable string or None.
- `title`: string or None.
- `subtitle`: string or None.
- `scrim`: `none`, `gradient`, or `solid`. Default None.
- `scrim_color`: string or None.
- `scrim_opacity`: number from 0.0 to 1.0. Default 1.0.

Additional `M3Carousel` fields:

- `is_extended`: bool or None.
- `free_scroll`: bool or None.
- `uncontained_item_extent`: float or None.
- `uncontained_shrink_extent`: float or None.
- `child_element_border_radius`: float or None.
- `large_max_width`: float or None.
- `item_padding`: float or None.
- `scroll_animation_duration`: int or None.
- `fixed_pulse_delta`: float, default 4.0.
- `single_swipe_gesture_sensitivity_range`: int or None.
- `haptic`: `none`, `light`, `medium`, or `heavy`. Default `none`.
- `header`: string or None.
- `show_all`: bool, default False.

Additional `M3CarouselItem` fields:

- `prefix_text`: string or None.
- `apply_dynamic_text_content_transform`: bool, default True.
- `aspect_ratio`: float, default 1.0.
- `semantic_label`: string or None.

`M3Carousel` async methods:

- `scroll_to(index=0)`
- `jump_to_item(index=0)`
- `animate_to_item(index=0)`
- `next()`
- `previous()`
- `show_all_items()`
