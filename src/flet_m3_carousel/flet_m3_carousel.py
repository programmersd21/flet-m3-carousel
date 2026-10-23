from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from flet.controls.base_control import control
from flet.controls.control_event import Event, EventHandler
from flet.controls.layout_control import LayoutControl

__all__ = [
    "M3Carousel",
    "M3CarouselChangeEvent",
    "M3CarouselEvent",
    "M3CarouselItem",
    "M3CarouselTapEvent",
    "serialize_items",
]

_LAYOUTS = ("hero", "contained", "uncontained", "uncontainedMultiAspect", "fullScreen")
_AXES = ("horizontal", "vertical")
_ALIGNMENTS = ("left", "center", "right")
_SCRIMS = ("none", "gradient", "solid")
_HAPTICS = ("none", "light", "medium", "heavy")

_LAYOUT_ALIASES = {
    "hero": "hero",
    "contained": "contained",
    "uncontained": "uncontained",
    "uncontainedmultiaspect": "uncontainedMultiAspect",
    "uncontained_multi_aspect": "uncontainedMultiAspect",
    "uncontained-multi-aspect": "uncontainedMultiAspect",
    "fullscreen": "fullScreen",
    "full_screen": "fullScreen",
    "full-screen": "fullScreen",
}


def _normalize_layout(value: Any) -> str:
    if not isinstance(value, str):
        raise TypeError(f"layout must be str, got {type(value).__name__}")
    normalized = value.strip().lower().replace(" ", "")
    canonical = _LAYOUT_ALIASES.get(normalized)
    if canonical is None:
        raise ValueError(f"layout must be one of {_LAYOUTS}, got {value!r}")
    return canonical


def _normalize_axis(value: Any) -> str:
    if not isinstance(value, str):
        raise TypeError(f"axis must be str, got {type(value).__name__}")
    normalized = value.strip().lower()
    if normalized not in _AXES:
        raise ValueError(f"axis must be one of {_AXES}, got {value!r}")
    return normalized


def _normalize_alignment(value: Any) -> str:
    if not isinstance(value, str):
        raise TypeError(f"hero_alignment must be str, got {type(value).__name__}")
    normalized = value.strip().lower()
    if normalized not in _ALIGNMENTS:
        raise ValueError(f"hero_alignment must be one of {_ALIGNMENTS}, got {value!r}")
    return normalized


def _normalize_scrim(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"scrim must be str or None, got {type(value).__name__}")
    normalized = value.strip().lower()
    if normalized not in _SCRIMS:
        raise ValueError(f"scrim must be one of {_SCRIMS}, got {value!r}")
    return normalized


def _normalize_haptic(value: Any) -> str:
    if not isinstance(value, str):
        raise TypeError(f"haptic must be str, got {type(value).__name__}")
    normalized = value.strip().lower()
    if normalized not in _HAPTICS:
        raise ValueError(f"haptic must be one of {_HAPTICS}, got {value!r}")
    return normalized


def _finite_number(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")
    number = float(value)
    if not number == number or number in (float("inf"), float("-inf")):
        raise ValueError(f"{name} must be finite, got {value!r}")
    return number


@dataclass
class M3CarouselItem:
    """One item in an :class:`M3Carousel`.

    Attributes:
        image: Image source. A URL, asset path, or base64-encoded data, as
            accepted by Flet's ``Image`` control.
        key: Stable identifier used to identify the item in events.
        title: Optional title text shown on large slots.
        subtitle: Optional supporting text shown under the title.
        scrim: Optional scrim style. One of ``"none"``, ``"gradient"``,
            or ``"solid"``.
        scrim_color: Color used when ``scrim`` is ``"solid"``.
        scrim_opacity: Opacity of the scrim, from ``0.0`` to ``1.0``.
    """

    image: str
    key: str | None = None
    title: str | None = None
    subtitle: str | None = None
    prefix_text: str | None = None
    scrim: str | None = None
    scrim_color: str | None = None
    scrim_opacity: float = 1.0
    apply_dynamic_text_content_transform: bool = True
    aspect_ratio: float = 1.0
    semantic_label: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.image, str):
            raise TypeError(f"image must be str, got {type(self.image).__name__}")
        if not self.image.strip():
            raise ValueError(f"image must be a non-empty str, got {self.image!r}")
        if self.key is not None and not isinstance(self.key, str):
            raise TypeError(f"key must be str or None, got {type(self.key).__name__}")
        if self.title is not None and not isinstance(self.title, str):
            raise TypeError(f"title must be str or None, got {type(self.title).__name__}")
        if self.subtitle is not None and not isinstance(self.subtitle, str):
            raise TypeError(f"subtitle must be str or None, got {type(self.subtitle).__name__}")
        if self.prefix_text is not None and not isinstance(self.prefix_text, str):
            raise TypeError(
                f"prefix_text must be str or None, got {type(self.prefix_text).__name__}"
            )
        if not isinstance(self.apply_dynamic_text_content_transform, bool):
            raise TypeError(
                "apply_dynamic_text_content_transform must be bool, "
                f"got {type(self.apply_dynamic_text_content_transform).__name__}"
            )
        number = _finite_number(self.aspect_ratio, "aspect_ratio")
        if number <= 0:
            raise ValueError(f"aspect_ratio must be positive, got {self.aspect_ratio!r}")
        if self.semantic_label is not None and not isinstance(self.semantic_label, str):
            raise TypeError(
                f"semantic_label must be str or None, got {type(self.semantic_label).__name__}"
            )
        self.scrim = _normalize_scrim(self.scrim)
        if self.scrim_color is not None and not isinstance(self.scrim_color, str):
            raise TypeError(
                f"scrim_color must be str or None, got {type(self.scrim_color).__name__}"
            )
        number = _finite_number(self.scrim_opacity, "scrim_opacity")
        if not 0.0 <= number <= 1.0:
            raise ValueError(
                f"scrim_opacity must be between 0.0 and 1.0, got {self.scrim_opacity!r}"
            )

    def to_dict(self) -> dict[str, Any]:
        """Serialize this item to a plain dictionary."""
        result: dict[str, Any] = {"image": self.image}
        if self.key is not None:
            result["key"] = self.key
        if self.title is not None:
            result["title"] = self.title
        if self.subtitle is not None:
            result["subtitle"] = self.subtitle
        if self.prefix_text is not None:
            result["prefix_text"] = self.prefix_text
        if self.scrim is not None and self.scrim != "none":
            result["scrim"] = self.scrim
            result["scrim_opacity"] = self.scrim_opacity
            if self.scrim_color is not None:
                result["scrim_color"] = self.scrim_color
        if not self.apply_dynamic_text_content_transform:
            result["apply_dynamic_text_content_transform"] = False
        if self.aspect_ratio != 1.0:
            result["aspect_ratio"] = self.aspect_ratio
        if self.semantic_label is not None:
            result["semantic_label"] = self.semantic_label
        return result


@dataclass
class M3CarouselTapEvent(Event["M3Carousel"]):
    """Payload for :attr:`M3Carousel.on_tap`."""

    index: int
    item_key: str | None = None


@dataclass
class M3CarouselChangeEvent(Event["M3Carousel"]):
    """Payload for :attr:`M3Carousel.on_change`."""

    index: int
    item_key: str | None = None


# Backwards-friendly alias.
M3CarouselEvent = M3CarouselTapEvent


def serialize_items(items: Sequence[M3CarouselItem]) -> list[dict[str, Any]]:
    """Serialize a sequence of carousel items to plain dictionaries."""
    if items is None:
        return []
    result: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, M3CarouselItem):
            raise TypeError(
                f"items must contain M3CarouselItem instances, got {type(item).__name__}"
            )
        result.append(item.to_dict())
    return result


@control("M3Carousel")  # type: ignore[arg-type]
class M3Carousel(LayoutControl):
    """A Flet control that wraps the Flutter ``m3_carousel`` package.

    The carousel layout and animation are delegated to the upstream
    package.
    """

    items: list[M3CarouselItem] = field(default_factory=list)
    layout: str = "hero"
    axis: str = "horizontal"
    hero_alignment: str = "center"
    is_extended: bool | None = None
    free_scroll: bool | None = None
    uncontained_item_extent: float | None = None
    uncontained_shrink_extent: float | None = None
    child_element_border_radius: float | None = None
    large_max_width: float | None = None
    item_padding: float | None = None
    scroll_animation_duration: int | None = None
    fixed_pulse_delta: float = 4.0
    single_swipe_gesture_sensitivity_range: int | None = None
    haptic: str = "none"
    header: str | None = None
    show_all: bool = False
    autoplay: bool = False
    autoplay_interval: int = 3000
    on_tap: EventHandler[M3CarouselTapEvent] | None = None
    on_change: EventHandler[M3CarouselChangeEvent] | None = None

    def __post_init__(self, ref: Any | None = None) -> None:
        # Normalize and validate scalar fields.
        self.layout = _normalize_layout(self.layout)
        self.axis = _normalize_axis(self.axis)
        self.hero_alignment = _normalize_alignment(self.hero_alignment)
        self.haptic = _normalize_haptic(self.haptic)

        if self.is_extended is not None and not isinstance(self.is_extended, bool):
            raise TypeError(
                f"is_extended must be bool or None, got {type(self.is_extended).__name__}"
            )
        if self.free_scroll is not None and not isinstance(self.free_scroll, bool):
            raise TypeError(
                f"free_scroll must be bool or None, got {type(self.free_scroll).__name__}"
            )
        if self.show_all is not None and not isinstance(self.show_all, bool):
            raise TypeError(f"show_all must be bool, got {type(self.show_all).__name__}")
        if not isinstance(self.autoplay, bool):
            raise TypeError(f"autoplay must be bool, got {type(self.autoplay).__name__}")
        if isinstance(self.autoplay_interval, bool) or not isinstance(self.autoplay_interval, int):
            raise TypeError("autoplay_interval must be int")
        if self.autoplay_interval <= 0:
            raise ValueError("autoplay_interval must be positive")
        for field_name in (
            "uncontained_item_extent",
            "uncontained_shrink_extent",
            "child_element_border_radius",
            "large_max_width",
            "item_padding",
            "fixed_pulse_delta",
        ):
            value = getattr(self, field_name)
            if value is not None:
                _finite_number(value, field_name)
        if self.uncontained_item_extent is not None and self.uncontained_item_extent <= 0:
            raise ValueError("uncontained_item_extent must be positive")
        if self.uncontained_shrink_extent is not None and self.uncontained_shrink_extent <= 0:
            raise ValueError("uncontained_shrink_extent must be positive")
        if self.fixed_pulse_delta is not None:
            _finite_number(self.fixed_pulse_delta, "fixed_pulse_delta")
        if self.scroll_animation_duration is not None:
            if isinstance(self.scroll_animation_duration, bool) or not isinstance(
                self.scroll_animation_duration, int
            ):
                raise TypeError("scroll_animation_duration must be int or None")
            if self.scroll_animation_duration < 0:
                raise ValueError("scroll_animation_duration must be non-negative")
        if self.single_swipe_gesture_sensitivity_range is not None:
            if isinstance(self.single_swipe_gesture_sensitivity_range, bool) or not isinstance(
                self.single_swipe_gesture_sensitivity_range, int
            ):
                raise TypeError("single_swipe_gesture_sensitivity_range must be int or None")
            if self.single_swipe_gesture_sensitivity_range < 0:
                raise ValueError("single_swipe_gesture_sensitivity_range must be non-negative")

        if self.items is None:
            self.items = []
        if not isinstance(self.items, (list, tuple)):
            raise TypeError(f"items must be a list or tuple, got {type(self.items).__name__}")
        normalized_items: list[M3CarouselItem] = []
        seen_keys: set[str] = set()
        for item in self.items:
            if not isinstance(item, M3CarouselItem):
                raise TypeError(
                    f"items must contain M3CarouselItem instances, got {type(item).__name__}"
                )
            if item.key is not None:
                if item.key in seen_keys:
                    raise ValueError(f"duplicate key: {item.key!r}")
                seen_keys.add(item.key)
            normalized_items.append(item)
        self.items = normalized_items

        super().__post_init__(ref)

    def serialize_items(self) -> list[dict[str, Any]]:
        return serialize_items(self.items)

    async def scroll_to(self, index: int = 0) -> None:
        await self._invoke_method("scroll_to", {"index": index})

    async def jump_to_item(self, index: int = 0) -> None:
        await self._invoke_method("jump_to_item", {"index": index})

    async def animate_to_item(self, index: int = 0) -> None:
        await self._invoke_method("animate_to_item", {"index": index})

    async def next(self) -> None:
        await self._invoke_method("next", {})

    async def previous(self) -> None:
        await self._invoke_method("previous", {})

    async def show_all_items(self) -> None:
        await self._invoke_method("show_all", {})

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "items": serialize_items(self.items),
            "layout": self.layout,
            "axis": self.axis,
            "hero_alignment": self.hero_alignment,
        }
        if self.is_extended is not None:
            result["is_extended"] = self.is_extended
        if self.free_scroll is not None:
            result["free_scroll"] = self.free_scroll
        if self.uncontained_item_extent is not None:
            result["uncontained_item_extent"] = self.uncontained_item_extent
        if self.uncontained_shrink_extent is not None:
            result["uncontained_shrink_extent"] = self.uncontained_shrink_extent
        if self.child_element_border_radius is not None:
            result["child_element_border_radius"] = self.child_element_border_radius
        if self.large_max_width is not None:
            result["large_max_width"] = self.large_max_width
        if self.item_padding is not None:
            result["item_padding"] = self.item_padding
        if self.scroll_animation_duration is not None:
            result["scroll_animation_duration"] = self.scroll_animation_duration
        if self.fixed_pulse_delta != 4.0:
            result["fixed_pulse_delta"] = self.fixed_pulse_delta
        if self.single_swipe_gesture_sensitivity_range is not None:
            result["single_swipe_gesture_sensitivity_range"] = (
                self.single_swipe_gesture_sensitivity_range
            )
        if self.haptic != "none":
            result["haptic"] = self.haptic
        if self.header is not None:
            result["header"] = self.header
        if self.show_all:
            result["show_all"] = True
        if self.autoplay:
            result["autoplay"] = True
            result["autoplay_interval"] = self.autoplay_interval
        return result
