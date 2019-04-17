import pytest
import os
from tools import imageComparison

folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), r"fixtures")
reference = os.path.join(folder, r"imageComparison_reference.jpg")
actual = os.path.join(folder, r"imageComparison_actual.jpg")
result = os.path.join(folder, r"imageComparison_result.jpg")
exclusions = [[0, 0, 0, 0]]


class TestToolsImageComparison:
    def test_same(self):
        assert imageComparison.compare_images(reference, reference, result, exclusions)

    def test_no_parameters(self):
        with pytest.raises(TypeError):
            imageComparison.compare_images()

    def test_empty_reference(self):
        with pytest.raises(AttributeError):
            imageComparison.compare_images("", actual, result, exclusions)

    def test_empty_actual(self):
        with pytest.raises(AttributeError):
            imageComparison.compare_images(reference, "", result, exclusions)

    def test_empty_result(self):
        with pytest.raises(ValueError):
            imageComparison.compare_images(reference, actual, "", exclusions)

    def test_empty_exclusions(self):
        assert imageComparison.compare_images(reference, actual, result, "") is not True

    def test_string_exclusions(self):
        with pytest.raises(TypeError):
            imageComparison.compare_images(reference, actual, result, "string")

    def test_two_exclusions(self):
        assert imageComparison.compare_images(
            reference, actual, result, [[45, 45, 245, 100], [485, 585, 940, 665]]
        )

    def test_one_exclusion(self):
        assert (
            imageComparison.compare_images(
                reference, actual, result, [[235, 180, 725, 535]]
            )
            is not True
        )
