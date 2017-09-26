import ctypes
import sys

fast_filter = ctypes.CDLL("libfast_filter.so")
if len(sys.argv) < 5:
	print "Please enter the correct number of arguments"
	sys.exit()
filter_width = int(sys.argv[3])
filter_weights = []
for i in range(4,len(sys.argv)):
	filter_weights.append(float(sys.argv[i]))
if len(filter_weights) != filter_width * filter_width:
	print "Please enter the correct number of arguments"
	sys.exit()
CFloatArrayType = ctypes.c_float * len(filter_weights)
cfloat_array_instance = CFloatArrayType( *filter_weights )

try:
	img = open(sys.argv[1], "r")
except IOError:
	print "Where that image at yo?"
	sys.exit()
else:
	input_img = img.read()
out_img_data = " " * len(input_img)
fast_filter.doFiltering(input_img, cfloat_array_instance, filter_width, out_img_data)

output_file = open(sys.argv[2], "w")
output_file.write(out_img_data)


