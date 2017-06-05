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

if len(sys.argv) >= 2:
        rule_number = int(sys.argv[1])

if len(sys.argv) >= 3:
        iterations = int(sys.argv[2])

if len(sys.argv) >= 4:
        for c in range(len(sys.argv[3])):
                for i in range(8):
                        data.append((ord(sys.argv[3][c]) >> (8 - i - 1)) % 2)
else:
        data = [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0]

output = array.array('i', (0,)*len(data))

total_output = 0

#   Open image here
image = Image.new("L", (cell_size * len(data), cell_size * iterations))

draw = ImageDraw.Draw(image)

for x in range(len(data)):
        if data[x] == 0:
                colour = ImageColor.getcolor("black", "L")
        else:
                colour = ImageColor.getcolor("white", "L")

        dim = (x * cell_size, 0)
                                            
        draw.rectangle([dim, (dim[0] + cell_size, dim[1] + cell_size)], colour)
        draw.rectangle([dim, (dim[0] + cell_size, dim[1] + cell_size)], outline=ImageColor.getcolor("grey", "L"))

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
	
	data = copy.deepcopy(output)

#   Add dotted borders

#   Save image here
image.save("C:/Users/John/Desktop/pattern.png", "PNG")
