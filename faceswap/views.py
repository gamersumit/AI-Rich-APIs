import numpy as np
import os
import glob
import cv2
import matplotlib.pyplot as plt

import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image

# Create your views here.

print('insightface', insightface.__version__)
print('numpy', np.__version__)
