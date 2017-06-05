# ElementaryCellularScarf
Small Python Script for creating knitting patterns based on elementary cellular automatons.

Only the input string is required, other values are specified with the following flags

-f (value): Specifies output file format, currently png, jpg, gif and bmp are accepted.

-i (value): The number of times to perform the rules (ie. the number of rows in the image) Defaults to 256 if not specified. Must be a positive integer.

-r (value): The rule to use; an integer between 0 and 255 inclusive. Defaults to 135 if not specified.

-m: Specifies if the image should be drawn twice, eg. if you're knitting a double-sided scarf and want the same pattern on each side. False by default.
