"""
Approach and methods of this module are loosely based on:
https://blog.rinatussenov.com/automating-manual-visual-regression-tests-with-python-and-selenium-be66be950196
"""
from PIL import Image, ImageDraw
import math
import functools
import operator


def compare_images(image_reference, image_actual, image_result, exclusions):
    """
    This compares 2 images (1 reference and 1 actual) and highlight the areas that are visually different
    :param image_reference: <string> : base image
    :param image_actual: <string> : image to compare against the base result
    :param image_result: <string> : image that highlights the differences
    :param exclusions: <array> : list of areas to be excluded from comparison
    :return: <bool> : True if image matches the base image
    """
    if exclusions == "":
        exclusions = [[0, 0, 0, 0]]
    passed = True
    image_reference = Image.open(image_reference)
    image_actual = Image.open(image_actual)
    columns = 60
    rows = 80
    image_width, image_height = image_reference.size
    block_width = ((image_width - 1) // columns) + 1
    block_height = ((image_height - 1) // rows) + 1

    # Looking at the histograms to quickly determine if there are differences in the two images
    reference_histogram = image_reference.histogram()
    actual_histogram = image_actual.histogram()
    root_mean_square = math.sqrt(
        functools.reduce(
            operator.add,
            map(lambda a, b: (a - b) ** 2, reference_histogram, actual_histogram),
        )
        / len(reference_histogram)
    )

    # If the histograms are different then do a more detailed pixel by pixel comparison
    if root_mean_square > 0:
        draw = ImageDraw.Draw(image_actual)
        pixel_include = []
        for x in range(image_width):
            column = []
            for y in range(image_height):
                column.append(0)
            pixel_include.append(column)

        for y in range(0, image_height, block_height + 1):
            for x in range(0, image_width, block_width + 1):
                pixel_include[x][y] = True
                region_reference = None
                region_actual = None

                for exclusion in exclusions:
                    if not (
                        exclusion[0] < x < exclusion[2]
                        and exclusion[1] < y < exclusion[3]
                    ):
                        region_reference = _process_image_region(
                            image_reference, x, y, block_width, block_height
                        )
                        region_actual = _process_image_region(
                            image_actual, x, y, block_width, block_height
                        )
                    else:
                        pixel_include[x][y] = False

                if (
                    region_reference is not None
                    and region_actual is not None
                    and region_actual != region_reference
                    and pixel_include[x][y] is True
                ):
                    passed = False
                    draw = ImageDraw.Draw(image_actual)
                    draw.rectangle(
                        (x, y, x + block_width, y + block_height), outline="red"
                    )

        for exclusion in exclusions:
            draw.rectangle(
                (exclusion[0], exclusion[1], exclusion[2], exclusion[3]),
                outline="green",
            )
        image_actual.save(image_result)

    return passed


def _process_image_region(image, x, y, width, height):
    """
    This will calculate the sum of pixel values for the specified image region
    :param image: <string> : image to get the pixel values from
    :param x: <int> : x coordinate of the region
    :param y: <int> : y coordinate of the region
    :param width: <int> : width of the region
    :param height: <int> : height of the region
    :return: <int> : weighted region_total
    """
    region_total = 0

    # This can be used as the sensitivity factor, the larger it is the less sensitive the comparison
    factor = 100

    for coordinateY in range(y, y + height):
        for coordinateX in range(x, x + width):
            try:
                pixel = image.getpixel((coordinateX, coordinateY))
                region_total += sum(pixel) / 4
            except Exception:
                return

    return region_total / factor


#############################################################################
# Main
#############################################################################
if __name__ == "__main__":
    compare_images(
        image_reference=r"C:\git_repos\pywinautomation\Projects\CCB_captureApp\ReferenceScreens\LoginPage-reference.jpg",
        image_actual=r"C:\git_repos\pywinautomation\Results\comparison_images\LoginPage-actual.jpg",
        image_result=r"C:\git_repos\pywinautomation\Results\comparison_images\LoginPage-result.jpg",
        exclusions=[0, 0, 0, 0],
    )
