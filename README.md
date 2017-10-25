# Show Stems

*This is a plugin for the [Glyphs font editor](http://glyphsapp.com/).*  

If active, it shows a measurement line (even in edit mode) with all distances between the outlines. If any distance matches the saved metrics in the Glyphs Palette, it will highlight in green and tell you which one it matches.
The vertical position is attached to the Glyphsapp measurement line and can be moved around the same way.

### How to use

When ever you need it, toggle `Show * Stems` from the view menu. There is a shortcut to (de)activate it:  
:point_right: `ctrl+alt+cmd+s` (like **S**tems)

### Examples
<p align="center">
<img src="https://github.com/Mark2Mark/Show-Stems/blob/master/Images/Show%20Stems%2001.gif" alt="Show Stems" height="500px">
</p>



##### Known Issues

- Q: It also highlights matching values *between* path-outlines. Keep/remove?
- Not sure about rounding values to integers. Perhaps 1 float point is better!? The info would be more accurate, but the stems entered in the palette will be integers anyway.
- the half xHeight/CapHeight indicator (left triangle) is horizontally a tiny bit off in italics. Cosmetic issue.

##### TODO

- Make it smarter to recognize non-Latin Settings.

##### Pull Requests

Feel free to comment or pull requests for any improvements.

##### License

Copyright 2016 [Mark Frömberg](http://www.markfromberg.com/) *@Mark2Mark*

Made possible with the GlyphsSDK by Georg Seifert (@schriftgestalt) and Rainer Erich Scheichelbauer (@mekkablue).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
