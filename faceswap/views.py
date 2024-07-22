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

class FaceSwapperAPIView(APIView):
   def post(self, request):
        source_file = request.FILES.get('source')  # full image
        target_file = request.FILES.get('target')  # face image results
        print("source:", source_file)
        print("target: ", target_file)
        if source_file and target_file:
            # Read source file content
            print("1")
            source_image_content = source_file.read()
            print("2")
            nparr_source = np.frombuffer(source_image_content, np.uint8)
            print("3")
            source_img = cv2.imdecode(nparr_source, cv2.IMREAD_COLOR)
            print("4")

            # Read target file content
            target_image_content = target_file.read()
            print("5")
            nparr_target = np.frombuffer(target_image_content, np.uint8)
            print("6")
            target_img = cv2.imdecode(nparr_target, cv2.IMREAD_COLOR)
            print("7")

            # Perform face swapping
            swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=False, download_zip=False)
            print("swappper ===>", swapper)
            print("8")
            app = insightface.app.FaceAnalysis(name='buffalo_l')
            print("9")
            app.prepare(ctx_id=0, det_size=(640, 640))
            print("10")

            face_source = app.get(source_img)[0]
            print("11")
            face_target = app.get(target_img)[0]
            print("12")

            swapped_face = swapper.get(source_img, face_source, face_target, paste_back=True)
            print("13")

            # Convert swapped face to bytes for upload
            _, swapped_face_bytes = cv2.imencode('.jpg', swapped_face)
            print("14")
            swapped_face_bytes = swapped_face_bytes.tobytes()
            print("15")

            #render image swapped_face_bytes
            # Save instance to the database
            # Save image to the static folder
            file_name = f'swapped_face_{uuid.uuid4().hex}.jpg'  # or generate a unique name if needed
            file_path = os.path.join(settings.STATIC_ROOT, file_name)

            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with default_storage.open(file_path, 'wb') as f:
                f.write(swapped_face_bytes)

            # Return the file URL
            file_url = os.path.join(settings.STATIC_URL, file_name)
            
            return Response({'status': 'Images processed successfully', 'file_url': file_url}, status=status.HTTP_200_OK)
        
        else:
            print("16")
            return Response({'error': 'Source or target image missing'}, status=status.HTTP_400_BAD_REQUEST)