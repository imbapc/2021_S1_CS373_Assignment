from matplotlib import pyplot

import imageIO.png


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


def main():
    filename = "./images/contrast/krakow.png"

    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(filename)

    pixel_array = [[] for i in range(len(px_array_r))]
    histogram_dict = {}

    for i in range(len(px_array_r)):
        for j in range(len(px_array_r[i])):
            n = round(0.299*px_array_r[i][j]+0.587*px_array_g[i][j]+0.114*px_array_b[i][j])
            pixel_array[i].append(n)
            if n not in histogram_dict:
                histogram_dict[n] = 1
            else:
                histogram_dict[n] = histogram_dict[n] + 1
    print(histogram_dict)

    fig1, axs1 = pyplot.subplots(1, 2)

    axs1[0].set_title('Input image')
    axs1[0].imshow(pixel_array, cmap='gray')

    # pyplot.show()

    dummy_histogram = [histogram_dict[i] for i in range(len(histogram_dict))]
    print(dummy_histogram)

    axs1[1].set_title('Histogram')
    axs1[1].bar(range(len(histogram_dict)), dummy_histogram)

    pyplot.show()


if __name__ == "__main__":
    main()
