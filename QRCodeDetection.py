
from matplotlib import pyplot
from matplotlib.patches import Rectangle

import imageIO.png


def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):

    new_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_array


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

def main():
    filename = "./images/covid19QRCode/poster1small.png"

    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(filename)

    #pyplot.imshow(prepareRGBImageForImshowFromIndividualArrays(px_array_r, px_array_g, px_array_b, image_width, image_height))

    greyscale_array = getGreyscalePixelArrayfromPixelArray(image_width, image_height, px_array_r, px_array_g, px_array_r)
    writeGreyscalePixelArraytoPNG("poster1small_grey.png", greyscale_array, image_width, image_height)
    horizontal_edge = getHorizontalEdges(image_width,image_height,greyscale_array)
    vertical_edge = getVerticalEdges(image_width, image_height, greyscale_array)
    gradient_magnitude = getGradientMagnitude(image_width,image_height,horizontal_edge,vertical_edge)
    gaussian_smooth = applyGaussianSmooth(image_width,image_height,gradient_magnitude)
    for i in range(5):
        gaussian_smooth = applyGaussianSmooth(image_width,image_height, gaussian_smooth)

    pyplot.imshow(gaussian_smooth, cmap='gray')

    # get access to the current pyplot figure
    axes = pyplot.gca()
    # create a 70x50 rectangle that starts at location 10,30, with a line width of 3
    rect = Rectangle( (130, 175), 450, 430, linewidth=3, edgecolor='g', facecolor='none')
    # paint the rectangle over the current plot
    axes.add_patch(rect)

    # plot the current figure
    pyplot.show()



if __name__ == "__main__":
    main()