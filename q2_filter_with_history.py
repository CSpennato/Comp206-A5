import sys
import pickle
import ctypes

fast_filter = ctypes.CDLL("libfast_filter.so")
if len(sys.argv) == 0:
	print "PLease specify the image operation you would like to implement. (load, filter, undo, redo)"
	sys.exit()

if sys.argv[1].lower() == "load":
	if len(sys.argv) != 3:
		print "Please provide an image"
		sys.exit()
	try:
		img = open(sys.argv[2], "r")
	except IOError:
		print "Please provide a valid image"
		sys.exit()
	else:
		active_img = img.read()
		output_file = open("result.bmp", "w")
		output_file.write(active_img)

elif sys.argv[1].lower() == "filter":
	try:
		img = open("result.bmp", "r")
	except IOError:
		print "Please load an image first"
		sys.exit()
	else:
		active_img = img.read()
	if len(sys.argv) < 4:
		print "Please provide a filter width and the appropriate number of filter weights"
		sys.exit()
	filter_weights = []
	filter_width = int(sys.argv[2])
	for i in range(3,len(sys.argv)):
		filter_weights.append(float(sys.argv[i]))
	if len(filter_weights) != filter_width * filter_width:
		print "Please enter the correct number of arguments"
		sys.exit()
	CFloatArrayType = ctypes.c_float * len(filter_weights)
	cfloat_array_instance = CFloatArrayType( *filter_weights )
	new_img = " " * len(active_img)
	fast_filter.doFiltering(active_img, cfloat_array_instance, filter_width, new_img)
	
	try:
		file = open("history.pickle", "rb")
	except IOError:
		file = open("history.pickle", "wb")
		images = [2, active_img, new_img]
		pickle.dump(images, file)
	else:
		images = pickle.load(file)
		if images[0] == len(images) - 1:
			images.append(new_img)
			images[0] = images[0] + 1
		else:
			images[0] = images[0] + 1
			images.insert(images[0], new_img)
			for i in range(0, len(images)-1 - images[0]):
				images.pop()
		file.close()
		file = open("history.pickle", "wb")
		pickle.dump(images, file)
		
	
	output_file = open("result.bmp", "w")
	output_file.write(new_img)
	

elif sys.argv[1].lower() == "undo":
	try:
		file = open("history.pickle", "rb")
	except IOError:
		print "Please load and filter an image before using the undo function"
		sys.exit()
	else:
		images = pickle.load(file)
		if images[0] > 1:
			images[0] = images[0] - 1
		else:
			print "Cannot undo anymore"
			sys.exit()
		file.close()
		file = open("history.pickle", "wb")
		pickle.dump(images, file)
		new_img = images[images[0]]
		output_file = open("result.bmp", "w")
		output_file.write(new_img)
elif sys.argv[1].lower() == "redo":
	try:
		file = open("history.pickle", "rb")
	except IOError:
		print "Please load and filter an image before using the redo function"
		sys.exit()
	else:
		images = pickle.load(file)
		if images[0] < len(images) - 1:
			images[0] = images[0] + 1
		else:
			print "Cannot redo anymore"
			sys.exit()
		file.close()
		file = open("history.pickle", "wb")
		pickle.dump(images, file)
		new_img = images[images[0]]
		output_file = open("result.bmp", "w")
		output_file.write(new_img)
else:
	print "PLease specify the image operation you would like to implement. (load, filter, undo, redo)"
	sys.exit()
