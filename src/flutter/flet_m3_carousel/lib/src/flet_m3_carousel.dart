import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:m3_carousel/m3_carousel.dart';

M3CarouselType layoutFromString(String? value) {
  final normalized = (value ?? 'hero')
      .trim()
      .toLowerCase()
      .replaceAll('_', '')
      .replaceAll('-', '');
  const mapping = <String, M3CarouselType>{
    'hero': M3CarouselType.hero,
    'contained': M3CarouselType.contained,
    'uncontained': M3CarouselType.uncontained,
    'uncontainedmultiaspect': M3CarouselType.uncontainedMultiAspect,
    'fullscreen': M3CarouselType.fullScreen,
  };
  final result = mapping[normalized];
  if (result == null) {
    throw ArgumentError(
      'Unknown M3Carousel layout: $value. '
      'Allowed: hero, contained, uncontained, uncontainedMultiAspect, fullScreen.',
    );
  }
  return result;
}

Axis axisFromString(String? value) {
  final normalized = (value ?? 'horizontal').trim().toLowerCase();
  if (normalized == 'horizontal') return Axis.horizontal;
  if (normalized == 'vertical') return Axis.vertical;
  throw ArgumentError(
    'Unknown M3Carousel axis: $value. Allowed: horizontal, vertical.',
  );
}

M3HeroAlignment heroAlignmentFromString(String? value) {
  final normalized = (value ?? 'center').trim().toLowerCase();
  for (final entry in M3HeroAlignment.values) {
    if (entry.name.toLowerCase() == normalized) return entry;
  }
  throw ArgumentError(
    'Unknown M3Carousel hero_alignment: $value. '
    'Allowed: left, center, right.',
  );
}

M3CarouselHapticFeedback hapticFromString(String? value) {
  final normalized = (value ?? 'none').trim().toLowerCase();
  for (final entry in M3CarouselHapticFeedback.values) {
    if (entry.name.toLowerCase() == normalized) return entry;
  }
  throw ArgumentError(
    'Unknown M3Carousel haptic: $value. '
    'Allowed: none, light, medium, heavy.',
  );
}

M3CarouselScrim? parseCarouselScrim(
  BuildContext context,
  Map<String, dynamic> item,
) {
  final scrim = item['scrim']?.toString();
  if (scrim == null || scrim.trim().isEmpty || scrim.toLowerCase() == 'none') {
    return null;
  }
  final opacity = (item['scrim_opacity'] as num?)?.toDouble() ?? 1.0;
  switch (scrim.toLowerCase()) {
    case 'gradient':
      return M3CarouselScrim.gradient(opacity: opacity);
    case 'solid':
      final colorValue = item['scrim_color']?.toString();
      final color = colorValue != null
          ? parseColor(colorValue, Theme.of(context))
          : null;
      return M3CarouselScrim(color: color ?? Colors.black, opacity: opacity);
    default:
      throw ArgumentError(
        'Unknown M3Carousel scrim: $scrim. '
        'Allowed: none, gradient, solid.',
      );
  }
}

class M3CarouselControl extends StatefulWidget {
  final Control control;

  const M3CarouselControl({super.key, required this.control});

  @override
  State<M3CarouselControl> createState() => _M3CarouselControlState();
}

class _M3CarouselControlState extends State<M3CarouselControl> {
  late final M3CarouselController _controller;

  @override
  void initState() {
    super.initState();
    _controller = M3CarouselController();
    widget.control.addInvokeMethodListener(_handleInvokeMethod);
  }

  @override
  void dispose() {
    widget.control.removeInvokeMethodListener(_handleInvokeMethod);
    _controller.dispose();
    super.dispose();
  }

  Future<dynamic> _handleInvokeMethod(String name, dynamic args) async {
    final map = args is Map
        ? Map<String, dynamic>.from(args)
        : <String, dynamic>{};
    switch (name) {
      case 'scroll_to':
      case 'animate_to_item':
        final index = (map['index'] as num?)?.toInt() ?? 0;
        await _controller.animateToItem(index);
        break;
      case 'jump_to_item':
        final index = (map['index'] as num?)?.toInt() ?? 0;
        _controller.jumpToItem(index);
        break;
      case 'next':
        await _controller.next();
        break;
      case 'previous':
        await _controller.previous();
        break;
      case 'show_all':
        _controller.showAll();
        break;
      default:
        break;
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    final control = widget.control;
    final layout = layoutFromString(control.getString('layout', 'hero'));
    final axis = axisFromString(control.getString('axis', 'horizontal'));
    final heroAlignment = heroAlignmentFromString(
      control.getString('hero_alignment', 'center'),
    );

    final width = control.getDouble('width');
    final height = control.getDouble('height');

    final isExtended = control.getBool('is_extended');
    final freeScroll = control.getBool('free_scroll');
    final uncontainedItemExtent = control.getDouble('uncontained_item_extent');
    final uncontainedShrinkExtent = control.getDouble(
      'uncontained_shrink_extent',
    );
    final childElementBorderRadius = control.getDouble(
      'child_element_border_radius',
    );
    final largeMaxWidth = control.getDouble('large_max_width');
    final itemPadding = control.getDouble('item_padding');
    final scrollAnimationDuration = control.getInt('scroll_animation_duration');
    final fixedPulseDelta = control.getDouble('fixed_pulse_delta', 4.0)!;
    final singleSwipeGestureSensitivityRange = control.getInt(
      'single_swipe_gesture_sensitivity_range',
    );
    final haptic = hapticFromString(control.getString('haptic', 'none'));
    final headerValue = control.getString('header');
    final showAll = control.getBool('show_all', false)!;

    final rawItems = control.get('items');
    final itemsList = rawItems is List ? rawItems : const <dynamic>[];

    final hasTapHandler = control.hasEventHandler('tap');

    final carouselItems = <M3CarouselItem>[];
    for (var i = 0; i < itemsList.length; i++) {
      final raw = itemsList[i];
      final item = raw is Map
          ? Map<String, dynamic>.from(raw)
          : <String, dynamic>{};

      final image = buildImage(
        context: context,
        src: item['image'],
        fit: BoxFit.cover,
        errorCtrl: null,
      );

      final titleValue = item['title'];
      final subtitleValue = item['subtitle'];
      final prefixValue = item['prefix_text'];
      final itemKey = item['key']?.toString();
      final scrim = parseCarouselScrim(context, item);
      final applyDynamic = item['apply_dynamic_text_content_transform'];
      final aspectRatio = (item['aspect_ratio'] as num?)?.toDouble();
      final semanticLabel = item['semantic_label']?.toString();

      carouselItems.add(
        M3CarouselItem(
          image: image,
          title: titleValue != null ? Text(titleValue.toString()) : null,
          subtitle: subtitleValue != null
              ? Text(subtitleValue.toString())
              : null,
          prefixText: prefixValue != null ? Text(prefixValue.toString()) : null,
          showScrim: scrim,
          applyDynamicTextContentTransform: applyDynamic is bool
              ? applyDynamic
              : true,
          aspectRatio: aspectRatio ?? 1.0,
          semanticLabel: semanticLabel,
          onTap: hasTapHandler
              ? () {
                  control.triggerEvent('tap', <String, dynamic>{
                    'index': i,
                    'item_key': itemKey,
                  });
                }
              : null,
        ),
      );
    }

    return LayoutControl(
      control: control,
      child: M3Carousel(
        controller: _controller,
        width: width,
        height: height,
        axis: axis,
        type: layout,
        isExtended: isExtended,
        freeScroll: freeScroll,
        heroAlignment: heroAlignment,
        uncontainedItemExtent:
            uncontainedItemExtent ??
            M3CarouselTheme.defaultUncontainedItemExtent,
        uncontainedShrinkExtent:
            uncontainedShrinkExtent ??
            M3CarouselTheme.defaultUncontainedShrinkExtent,
        childElementBorderRadius: childElementBorderRadius,
        largeMaxWidth: largeMaxWidth,
        itemPadding: itemPadding != null ? EdgeInsets.all(itemPadding) : null,
        scrollAnimationDuration:
            scrollAnimationDuration ??
            M3CarouselTheme.defaultScrollAnimationDuration,
        fixedPulseDelta: fixedPulseDelta,
        singleSwipeGestureSensitivityRange:
            singleSwipeGestureSensitivityRange ??
            M3CarouselTheme.defaultSingleSwipeGestureSensitivityRange,
        haptic: haptic,
        header: headerValue != null ? Text(headerValue) : null,
        showAll: showAll,
        onChange: control.hasEventHandler('change')
            ? (M3CarouselChangeDetails details) {
                final index = details.focalIndex;
                String? itemKey;
                if (index >= 0 && index < itemsList.length) {
                  final raw = itemsList[index];
                  if (raw is Map) {
                    itemKey = raw['key']?.toString();
                  }
                }
                control.triggerEvent('change', <String, dynamic>{
                  'index': index,
                  'item_key': itemKey,
                });
              }
            : null,
        children: carouselItems,
      ),
    );
  }
}
