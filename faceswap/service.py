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
from django.http import HttpResponse, JsonResponse
from PIL import Image, ImageDraw, ImageFont
import io
import base64

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
    

class TextOverlay:

    def overlay_text_on_image(self, image, text = 'BA BA BLACK SHEEP   BA BA BLACK SHEEP'):
        # Get image data from request (assuming it's a base64 encoded string)
        print("start ===>")
        # Decode the base64 image data
        image_data = image.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGBA")
        txt_layer = Image.new('RGBA', image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        # Define text and font
        font_path = '/home/sumit/Documents/GitHub/AI-Rich-APIs/BENG.TTF'  # Optional: specify a font
        font = ImageFont.truetype(font_path, size=20)  # Adjust size as needed

        # Calculate text size and position
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x, y = 50, 50  # Adjust as needed

        # Calculate dynamic position based on image size
        image_width, image_height = image.size
        margin = 30  # Adjust as needed
        x = (image_width - text_width) / 2
        y = image_height - text_height - margin

        # Define the background box
        box_padding = 10
        box = [x - box_padding, y - box_padding, x + text_width + box_padding, y + text_height + box_padding]

        # Draw the rounded rectangle
        radius = 20  # Adjust as needed
        draw.rounded_rectangle(box, radius=radius, fill=(255, 255, 255, 130))

        # Draw the text on top of the box
        draw.text((x, y), text, font=font, fill="black")  # Adjust fill color as needed

        combined = Image.alpha_composite(image, txt_layer)
        # Save to a BytesIO object
        img_byte_arr = io.BytesIO()
        combined.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # Return the image as HTTP response
        return HttpResponse(img_byte_arr, content_type='image/png')
