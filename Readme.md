# Image Comparison with Python

## Introduction
A basic approach for comparing two images. Particularly handy for visual regression testing.

To get all relevant packages:
```cmd
pip install -r ./requirements/base.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

## Basic usage
This will do a basic comparison
```python
from tools import imageComparison
imageComparison.compare_images("imageComparison_reference.jpg", "imageComparison_actual.jpg", "imageComparison_result.jpg")
```

## Using exclusion zones
Handy for when you want to exclude sections of the image (i.e. for parts of an image that contain changing bits like date/time).

Exclusions zones are specified as rectangled coordinates (pixels)
```python
from tools import imageComparison
imageComparison.compare_images("imageComparison_reference.jpg", "imageComparison_actual.jpg", "imageComparison_result.jpg", [[45, 45, 245, 100], [485, 585, 940, 665]])
```