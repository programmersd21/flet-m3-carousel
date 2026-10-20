import pytest

from flet_m3_carousel import (
    M3Carousel,
    M3CarouselChangeEvent,
    M3CarouselItem,
    M3CarouselTapEvent,
    serialize_items,
)


def test_imports() -> None:
    assert M3Carousel is not None
    assert M3CarouselItem is not None


def test_defaults() -> None:
    c = M3Carousel()
    assert c.items == []
    assert c.layout == "hero"
    assert c.axis == "horizontal"
    assert c.hero_alignment == "center"
    assert c.on_tap is None
    assert c.on_change is None


def test_item_defaults() -> None:
    item = M3CarouselItem(image="x.jpg")
    assert item.key is None
    assert item.title is None
    assert item.subtitle is None
    assert item.scrim is None


def test_invalid_layout() -> None:
    with pytest.raises(ValueError, match="layout"):
        M3Carousel(layout="nope")


def test_invalid_axis() -> None:
    with pytest.raises(ValueError, match="axis"):
        M3Carousel(axis="diagonal")


def test_invalid_alignment() -> None:
    with pytest.raises(ValueError, match="hero_alignment"):
        M3Carousel(hero_alignment="top")


def test_item_missing_image() -> None:
    with pytest.raises((ValueError, TypeError)):
        M3CarouselItem(image="")


def test_item_wrong_type() -> None:
    with pytest.raises(TypeError):
        M3CarouselItem(image=123)  # type: ignore[arg-type]


def test_duplicate_key() -> None:
    with pytest.raises(ValueError, match="duplicate key"):
        M3Carousel(
            items=[
                M3CarouselItem(key="a", image="x"),
                M3CarouselItem(key="a", image="y"),
            ]
        )


def test_serialized_output() -> None:
    c = M3Carousel(items=[M3CarouselItem(key="a", image="x.jpg", title="T", subtitle="S")])
    assert serialize_items(c.items) == [
        {"image": "x.jpg", "key": "a", "title": "T", "subtitle": "S"}
    ]


def test_event_fields() -> None:
    e = M3CarouselTapEvent(control=None, name="tap", index=2, item_key="k")  # type: ignore[arg-type]
    assert e.index == 2
    assert e.item_key == "k"
    e2 = M3CarouselChangeEvent(control=None, name="change", index=1, item_key=None)  # type: ignore[arg-type]
    assert e2.index == 1
    assert e2.item_key is None
