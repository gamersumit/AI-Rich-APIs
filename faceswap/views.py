from django.http import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.views import APIView
import cv2
import numpy as np
from .models import Face_Swap
from .utils import upload_image_to_s3
import insightface
from rest_framework import status

class FaceSwapperAPIView(APIView):
   def post(self, request):
        source_file = request.FILES.get('source')
        target_file = request.FILES.get('target')
        print("source:", source_file)
        print("target: ", target_file)
        if source_file and target_file:
            # Read source file content
            source_image_content = source_file.read()
            nparr_source = np.frombuffer(source_image_content, np.uint8)
            source_img = cv2.imdecode(nparr_source, cv2.IMREAD_COLOR)

            # Read target file content
            target_image_content = target_file.read()
            nparr_target = np.frombuffer(target_image_content, np.uint8)
            target_img = cv2.imdecode(nparr_target, cv2.IMREAD_COLOR)

            # Perform face swapping
            swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=False, download_zip=False)
            app = insightface.app.FaceAnalysis(name='buffalo_l')
            app.prepare(ctx_id=0, det_size=(640, 640))

            face_source = app.get(source_img)[0]
            face_target = app.get(target_img)[0]

            swapped_face = swapper.get(source_img, face_source, face_target, paste_back=True)

            # Convert swapped face to bytes for upload
            _, swapped_face_bytes = cv2.imencode('.jpg', swapped_face)
            swapped_face_bytes = swapped_face_bytes.tobytes()

            #render image swapped_face_bytes
            # Save instance to the database


            return Response({'status': 'Images processed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Source or target image missing'}, status=status.HTTP_400_BAD_REQUEST)