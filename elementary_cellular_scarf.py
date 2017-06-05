from PIL import Image, ImageDraw, ImageColor
import copy
import array
import sys

#	01001010 - J
#	01011010 - Z
#	01000110 - F

#	Rule 135 is defined as follows:
#	10000111
#	111 - 1
#	110 - 0
#	101 - 0
#	100 - 0
#	011 - 0
#	010 - 1
#	001 - 1
#	000 - 1

#data = [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0]
data = []

rule_number = 135

counter = 0

cell_size = 16
iterations = 256

valid_formats = ["bmp", "jpg", "png", "gif"]

output_format = "png"

#       TODO: Change input to be flag based
#       Search for flags in input values (eg. -f)
#       And then look for next value to see if it's valid.
#       Eg. if a parameter is -f, then check to see if the next parameter is an applicable format

#       Input seed value
if len(sys.argv) >= 2:
        if len(sys.argv[1]) == 0:
                print("Initial value must not be empty")
                sys.exit()
                
        for c in range(len(sys.argv[1])):
                for i in range(8):
                        data.append((ord(sys.argv[1][c]) >> (8 - i - 1)) % 2)
else:
        print("You must provide an input value")
        sys.exit()

#       -f flag determines output format
#       Following value expected to be valid file extension
if "-f" in sys.argv:
        index = sys.argv.index("-f")
        if len(sys.argv) > index + 1:
                output_format = sys.argv[index + 1]
        else:
                print("You must provide a valid format with the -f flag")
                sys.exit()

#       -i flag determines number of iterations
#       Following value expected to be positive integer
if "-i" in sys.argv:
        index = sys.argv.index("-i")
        if len(sys.argv) > index + 1:
                iterations = int(sys.argv[index + 1])
                
                if iterations < 1:
                        print("You need at least 1 iteration")
                        sys.exit()

#       -r flag determines rule number
#       Following value expected to be integer between 0 and 255 inclusive
if "-r" in sys.argv:
        index = sys.argv.index("-r")

        if len(sys.argv) > index + 1:
                rule_number = int(sys.argv[index + 1])

                if rule_number < 0 or rule_number > 255:
                        print("Rule number must be between 0 and 255 inclusive")
                        sys.exit()

mirror = False

#       Input whether or not to mirror the pattern
if "-m" in sys.argv:
        mirror = True

output = array.array('i', (0,)*len(data))

total_output = 0

#   Open image here
#       If mirror, then make it twice as large
image = Image.new("L", (cell_size * len(data) * (2 if mirror else 1), cell_size * iterations))

draw = ImageDraw.Draw(image)

#       Drawing first line
for x in range(len(data)):
        if data[x] == 0:
                colour = ImageColor.getcolor("black", "L")
        else:
                colour = ImageColor.getcolor("white", "L")

        dim = (x * cell_size, 0)
                                            
        draw.rectangle([dim, (dim[0] + cell_size, dim[1] + cell_size)], colour)
        draw.rectangle([dim, (dim[0] + cell_size, dim[1] + cell_size)], outline=ImageColor.getcolor("grey", "L"))

        if mirror:
                draw.rectangle([(dim[0] + (len(data) * cell_size), dim[1]), (dim[0] + (len(data) * cell_size) + cell_size, dim[1] + cell_size)], colour)
                draw.rectangle([(dim[0] + (len(data) * cell_size), dim[1]), (dim[0] + (len(data) * cell_size) + cell_size, dim[1] + cell_size)], outline=ImageColor.getcolor("grey", "L"))
                

#       Drawing remaining lines
for j in range(1,iterations):
	for i in range(len(data)):
		#   Python handles negative array indices,
		#   so I don't need to worry about edge cases
		#   General case
		val = data[i-1] * 4 + data[i] * 2 + data[(i + 1) % len(data)]

		output[i] = (rule_number >> val) % 2

		#   Write cell to image here

		if output[i] == 0:
			colour = ImageColor.getcolor("black", "L")
		else:
			colour = ImageColor.getcolor("white", "L")

		dim = (i * cell_size, j * cell_size)
				
		draw.rectangle([dim, (dim[0] + cell_size, dim[1] + cell_size)], colour)
		draw.rectangle([dim, (dim[0] + cell_size, dim[1] + cell_size)], outline=ImageColor.getcolor("grey", "L"))

		if mirror:
                        draw.rectangle([(dim[0] + (len(data) * cell_size), dim[1]), (dim[0] + (len(data) * cell_size) + cell_size, dim[1] + cell_size)], colour)
                        draw.rectangle([(dim[0] + (len(data) * cell_size), dim[1]), (dim[0] + (len(data) * cell_size) + cell_size, dim[1] + cell_size)], outline=ImageColor.getcolor("grey", "L"))
                
	data = copy.deepcopy(output)

#   Add dotted borders

#   Save image here
image.save("pattern.{0}".format(output_format), output_format)
