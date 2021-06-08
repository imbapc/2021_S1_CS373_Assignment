
from matplotlib import pyplot
from matplotlib.patches import Rectangle, Polygon
from pyzbar.pyzbar import decode
import os

import imageIO.png



#This is the queue class for Connected Conponent
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):

    new_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_array


# This method applies dilation
def applyDilation(pixel_array, w, h):
    dilation_array = createInitializedGreyscalePixelArray(w, h)
    for i in range(h):
        for j in range(w):
            if not pixel_array[i][j] == 0:
                dilation_array[i][j] = 1
                if not j - 1 < 0:
                    dilation_array[i][j - 1] = 1
                if j + 1 < w:
                    dilation_array[i][j + 1] = 1
                if not i - 1 < 0:
                    dilation_array[i - 1][j] = 1
                    if not j - 1 < 0:
                        dilation_array[i - 1][j - 1] = 1
                    if  j + 1 < w:
                        dilation_array[i - 1][j + 1] = 1
                if i + 1 < h:
                    dilation_array[i + 1][j] = 1
                    if not j - 1 < 0:
                        dilation_array[i + 1][j - 1] = 1
                    if j + 1 < w:
                        dilation_array[i + 1][j + 1] = 1

    return dilation_array


# This method applies erosion
def applyErosion(pixel_array, w, h):
    kernel_array = createInitializedGreyscalePixelArray(w, h)
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            if pixel_array[i - 1][j - 1] == 0 or pixel_array[i - 1][j] == 0 or pixel_array[i - 1][j + 1] == 0 \
                    or pixel_array[i][j - 1] == 0 or pixel_array[i][j] == 0 or pixel_array[i][j + 1] == 0 \
                    or pixel_array[i + 1][j - 1] == 0 or pixel_array[i + 1][j] == 0 or pixel_array[i + 1][j + 1] == 0:
                kernel_array[i][j] = 0
            else:
                kernel_array[i][j] = 1

    return kernel_array


# this function reads an RGB color png file and returns width, height, as well as pixel arrays for r,g,b
def readRGBImageToSeparatePixelArrays(input_filename):

    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)


# This method packs together three individual pixel arrays for r, g and b values into a single array that is fit for
# use in matplotlib's imshow method
def prepareRGBImageForImshowFromIndividualArrays(r,g,b,w,h):
    rgbImage = []
    for y in range(h):
        row = []
        for x in range(w):
            triple = []
            triple.append(r[y][x])
            triple.append(g[y][x])
            triple.append(b[y][x])
            row.append(triple)
        rgbImage.append(row)
    return rgbImage


# This method takes a greyscale pixel array and writes it into a png file
def writeGreyscalePixelArraytoPNG(output_filename, pixel_array, image_width, image_height):
    # now write the pixel array as a greyscale png
    file = open(output_filename, 'wb')  # binary mode is important
    writer = imageIO.png.Writer(image_width, image_height, greyscale=True)
    writer.write(file, pixel_array)
    file.close()


# This method takes image width, height and pixel array for red, green and blue and write a greyscale pixel array.
def getGreyscalePixelArrayfromPixelArray(w,h,r,g,b):
    result_array = createInitializedGreyscalePixelArray(w,h)
    for i in range(h):
        for j in range(w):
            n = round(0.299 * r[i][j] + 0.587 * g[i][j] + 0.114 * b[i][j])
            result_array[i][j] = n
    print(result_array)
    return result_array


# This method takes image width, height and the greyscale and calculate the horizontal edges of the image
def getHorizontalEdges(w,h,g):
    result_array = createInitializedGreyscalePixelArray(w, h)
    for i in range(1,h-1):
        for j in range(1,w-1):
            result_array[i][j] = round((g[i-1][j-1]*1+g[i-1][j]*2+g[i-1][j+1]*1-g[i+1][j-1]*1-g[i+1][j]*2-g[i+1][j+1]*1)/8)

    return result_array


# This method takes image width, height and the greyscale and calculate the vertical edges of the image
def getVerticalEdges(w,h,g):
    result_array = createInitializedGreyscalePixelArray(w, h)
    for i in range(1,h-1):
        for j in range(1,w-1):
            result_array[i][j] = round((g[i-1][j+1]*1+g[i][j+1]*2+g[i+1][j+1]*1-g[i-1][j-1]*1-g[i][j-1]*2-g[i+1][j-1]*1)/8)

    return result_array


# This method takes image width, height, and both horizontal and vertical edges, return the gradient magnitude of the
# image
def getGradientMagnitude(w,h,horizontal,vertical):
    result_array = createInitializedGreyscalePixelArray(w,h)
    for i in range(h):
        for j in range(w):
            result_array[i][j] = abs(horizontal[i][j])+abs(vertical[i][j])

    return result_array


# This method takes image width, height and the gradient magnitude and apply a Gaussian smooth to it
def applyGaussianSmooth(w,h,g):
    result_array = createInitializedGreyscalePixelArray(w,h)
    for i in range(1,h-1):
        for j in range(1,w-1):
           result_array[i][j] = round((g[i-1][j-1]*1+g[i-1][j]*2+g[i-1][j+1]*1+g[i][j-1]*2+g[i][j]*4+g[i][j+1]*2+g[i+1][
              j-1]*1+ g[i+1][j]*2+g[i+1][j+1]*1)/16)
#            result_array[i][j] = round((g[i-1][j-1]+g[i-1][j]+g[i-1][j+1]+g[i][j-1]+g[i][j]+g[i][j+1]+g[i+1][j-1]+g[i+1][j]+g[i+1][j+1])/9)

    return result_array


# This method takes image width, height and a greyscale array and apply thresholding operation with thresholding number 1
# and return the result array
def applyThresholdingOperation(w,h,g,t=20):
    result_array = createInitializedGreyscalePixelArray(w,h)
    for i in range(h):
        for j in range(w):
            if g[i][j] < t:
                result_array[i][j] = 0
            else:
                result_array[i][j] = 255

    return result_array


# This method applies a morphological closing operation
def applyClosing(pixel_array, w, h):
    for i in range(10):
        dilation = applyDilation(pixel_array, w, h)
    for i in range(10):
        erosion = applyErosion(dilation, w, h)
    return erosion


# This method takes image width, height and a binary greyscale array and get all the connnected objects.
def computeConnectedComponentLabeling(pixel_array, w, h):
    result_array = createInitializedGreyscalePixelArray(w, h)
    visited_pixel = createInitializedGreyscalePixelArray(w, h)
    key = 1
    result_dict = {}
    for i in range(h):
        for j in range(w):
            if pixel_array[i][j] != 0 and visited_pixel[i][j] == 0:
                value = pixel_array[i][j]
                queue = Queue()
                queue.enqueue([i,j])
                result_array[i][j] = key
                visited_pixel[i][j] = 255
                result_dict[key] = 1
                while not queue.isEmpty():
                    index = queue.dequeue()
                    if index[0]-1 in range(h) and index[1] in range(w):
                        if pixel_array[index[0]-1][index[1]] != 0 and visited_pixel[index[0]-1][index[1]] == 0:
                            queue.enqueue([index[0]-1, index[1]])
                            visited_pixel[index[0]-1][index[1]] = 1
                            result_array[index[0]-1][index[1]] = key
                            result_dict[key] = result_dict[key] + 1
                    if index[0] in range(h) and index[1]-1 in range(w):
                        if pixel_array[index[0]][index[1]-1] != 0 and visited_pixel[index[0]][index[1]-1] == 0:
                            queue.enqueue([index[0], index[1]-1])
                            visited_pixel[index[0]][index[1]-1] = 1
                            result_array[index[0]][index[1]-1] = key
                            result_dict[key] = result_dict[key] + 1
                    if index[0] in range(h) and index[1]+1 in range(w):
                        if pixel_array[index[0]][index[1]+1] != 0 and visited_pixel[index[0]][index[1]+1] == 0:
                            queue.enqueue([index[0], index[1]+1])
                            visited_pixel[index[0]][index[1]+1] = 1
                            result_array[index[0]][index[1]+1] = key
                            result_dict[key] = result_dict[key] + 1
                    if index[0]+1 in range(h) and index[1] in range(w):
                        if pixel_array[index[0]+1][index[1]] != 0 and visited_pixel[index[0]+1][index[1]] == 0:
                            queue.enqueue([index[0]+1, index[1]])
                            visited_pixel[index[0]+1][index[1]] = 1
                            result_array[index[0]+1][index[1]] = key
                            result_dict[key] = result_dict[key] + 1
                key = key + 1
    return (result_array, result_dict)


# This method detects four vortexes of possible object from a binary array
def computeVortexes(pixel_array, w, h):
    min_h = h
    min_w = w
    max_h = 0
    max_w = 0

    for i in range(h):
        for j in range(w):
            if pixel_array[i][j] == 1:
                if min_w > j:
                    min_w = j
                if max_w < j:
                    max_w = j
                if min_h > i:
                    min_h = i
                if max_h < i:
                    max_h = i
    return (min_w, min_h, max_w, max_h)


#This method defines the biggest object in the picture
def computeMainObject(pixel_array, array_dict, w, h):
    max = 0
    num = 0
    result_array = createInitializedGreyscalePixelArray(w, h)
    for key in array_dict:
        if array_dict[key] > max:
            max = array_dict[key]
            num = key
    for i in range(h):
        for j in range(w):
            if pixel_array[i][j] != num:
                result_array[i][j] = 0
            else:
                result_array[i][j] = 1
    return result_array


#This method return the edge of pixel_array
def computeMainObjectEdge(pixel_array, w, h):
    result_array = createInitializedGreyscalePixelArray(w, h)
    for i in range(h):
        for j in range(w):
            if not pixel_array[i][j] == 0:
                if not j - 1 < 0:
                    result_array[i][j - 1] = 1 - pixel_array[i][j - 1]
                if j + 1 < w:
                    result_array[i][j + 1] = 1 - pixel_array[i][j + 1]
                if not i - 1 < 0:
                    result_array[i - 1][j] = 1 - pixel_array[i - 1][j]
                    if not j - 1 < 0:
                        result_array[i - 1][j - 1] = 1 - pixel_array[i - 1][j - 1]
                    if j + 1 < w:
                        result_array[i - 1][j + 1] = 1 - pixel_array[i - 1][j + 1]
                if i + 1 < h:
                    result_array[i + 1][j] = 1 - pixel_array[i + 1][j]
                    if not j - 1 < 0:
                        result_array[i + 1][j - 1] = 1 - pixel_array[i + 1][j - 1]
                    if j + 1 < w:
                        result_array[i + 1][j + 1] = 1 - pixel_array[i + 1][j + 1]

    return result_array


def main():
    os.add_dll_directory("D:/project/venv/lib/site-packages/pyzbar")
    filename = "./images/covid19QRCode/poster1small.png"

    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(filename)

    pyplot.imshow(prepareRGBImageForImshowFromIndividualArrays(px_array_r, px_array_g, px_array_b, image_width, image_height))

    greyscale_array = getGreyscalePixelArrayfromPixelArray(image_width, image_height, px_array_r, px_array_g, px_array_r)
    #writeGreyscalePixelArraytoPNG("poster1smallrotated.png", greyscale_array, image_width, image_height)
    horizontal_edge = getHorizontalEdges(image_width,image_height,greyscale_array)
    vertical_edge = getVerticalEdges(image_width, image_height, greyscale_array)
    gradient_magnitude = getGradientMagnitude(image_width,image_height,horizontal_edge,vertical_edge)
    gaussian_smooth = applyGaussianSmooth(image_width,image_height,gradient_magnitude)
    for i in range(10):
        gaussian_smooth = applyGaussianSmooth(image_width,image_height, gaussian_smooth)
    thresholding_operation = applyThresholdingOperation(image_width,image_height,gaussian_smooth)
    closing_array = applyClosing(thresholding_operation, image_width, image_height)
    (connected_array, array_dict) = computeConnectedComponentLabeling(closing_array, image_width, image_height)
    main_object = computeMainObject(connected_array,array_dict,image_width,image_height)
    (min_w, min_h, max_w, max_h) = computeVortexes(main_object, image_width, image_height)
    main_object_edge = computeMainObjectEdge(main_object, image_width, image_height)

    #pyplot.imshow(main_object_edge, cmap='gray')


    # get access to the current pyplot figure
    axes = pyplot.gca()
    # create a 70x50 rectangle that starts at location 10,30, with a line width of 3
    rect = Rectangle((min_w-3, min_h-3), (max_w-min_w)+6, (max_h-min_h)+6, linewidth=3, edgecolor='g', facecolor='none')
    # paint the rectangle over the current plot
    axes.add_patch(rect)
    decode(greyscale_array.tobytes(), image_width, image_height)

    # plot the current figure
    pyplot.show()



if __name__ == "__main__":
    main()