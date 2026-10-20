import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:m3_carousel/m3_carousel.dart';
import 'package:flet_m3_carousel/src/flet_m3_carousel.dart';

void main() {
  group('layoutFromString', () {
    test('maps every layout', () {
      expect(layoutFromString('hero'), M3CarouselType.hero);
      expect(layoutFromString('contained'), M3CarouselType.contained);
      expect(layoutFromString('uncontained'), M3CarouselType.uncontained);
      expect(layoutFromString('uncontainedMultiAspect'),
          M3CarouselType.uncontainedMultiAspect);
      expect(layoutFromString('fullScreen'), M3CarouselType.fullScreen);
    });

    test('rejects unknown', () {
      expect(() => layoutFromString('nope'), throwsArgumentError);
    });
  });

  group('axisFromString', () {
    test('maps axes', () {
      expect(axisFromString('horizontal'), Axis.horizontal);
      expect(axisFromString('vertical'), Axis.vertical);
    });

    test('rejects unknown', () {
      expect(() => axisFromString('diagonal'), throwsArgumentError);
    });
  });

  group('heroAlignmentFromString', () {
    test('maps alignments', () {
      expect(heroAlignmentFromString('left'), M3HeroAlignment.left);
      expect(heroAlignmentFromString('center'), M3HeroAlignment.center);
      expect(heroAlignmentFromString('right'), M3HeroAlignment.right);
    });

    test('rejects unknown', () {
      expect(() => heroAlignmentFromString('top'), throwsArgumentError);
    });
  });

  group('parseCarouselScrim', () {
    test('none returns null', () {
      expect(parseCarouselScrim(const _FakeContext(), {'scrim': 'none'}), isNull);
    });

    test('gradient returns scrim', () {
      final scrim = parseCarouselScrim(const _FakeContext(), {'scrim': 'gradient'});
      expect(scrim, isNotNull);
      expect(scrim!.isGradient, isTrue);
    });

    test('rejects unknown', () {
      expect(
        () => parseCarouselScrim(const _FakeContext(), {'scrim': 'sparkles'}),
        throwsArgumentError,
      );
    });
  });
}

class _FakeContext implements BuildContext {
  const _FakeContext();

  @override
  dynamic noSuchMethod(Invocation invocation) => null;
}
