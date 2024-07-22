import os
import uuid
from django.http import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.views import APIView
import cv2
import numpy as np
import insightface
from rest_framework import status
from django.core.files.storage import default_storage
from core import settings
from faceswap.models import FaceSwap
from utils.cloudinary import Cloudinary 


class InsightFaceService :
    def __init__(self):
        self.swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=False, download_zip=False)
        self.app = insightface.app.FaceAnalysis(name='buffalo_l')
        self.app.prepare(ctx_id=0, det_size=(640, 640))


    def start_swap(self, source, target):
        decoded_target = self.decode_image(image=target)
        decoded_source = self.decode_image(image=source)
        source_face = self.get_face(decoded_image=decoded_source)
        target_face = self.get_face(decoded_image=decoded_target)
        return self.swap_face(source_img=decoded_source, face_source=source_face, face_target=target_face)


    def decode_image(self, image):
        image_content = image.read()
        nparr_source = np.frombuffer(image_content, np.uint8)
        return cv2.imdecode(nparr_source, cv2.IMREAD_COLOR)
    
    def get_face(self, decoded_image):
        return self.app.get(decoded_image)[0]

    def swap_face(self, source_img, face_source, face_target):
        swapped_face = self.swapper.get(source_img, face_source, face_target, paste_back=True)
        
        # Convert swapped face to bytes for upload
        _, swapped_face_bytes = cv2.imencode('.jpg', swapped_face)
        return swapped_face_bytes.tobytes()
        