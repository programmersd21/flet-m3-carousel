import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

import 'flet_m3_carousel.dart';

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "M3Carousel":
        return M3CarouselControl(key: key, control: control);
      default:
        return null;
    }
  }
}
