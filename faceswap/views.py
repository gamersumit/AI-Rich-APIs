from io import BytesIO
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from faceswap.models import FaceSwap
from faceswap.service import InsightFaceService
from utils.cloudinary import Cloudinary 


class FaceSwapperAPIView(APIView):
   def post(self, request):
        try :
            swap = InsightFaceService()
            source_file = request.FILES.get('source').read()  # full image
            target_file = request.FILES.get('target').read()  # face image results
            swapped_file = swap.start_swap(source = BytesIO(source_file), target = BytesIO(target_file))    

            # UPLOAD TO CLODINARY
            source_face = Cloudinary.UploadMediaToCloud(media = BytesIO(source_file))
            target_face = Cloudinary.UploadMediaToCloud(media = BytesIO(target_file))
            swapped_face = Cloudinary.UploadMediaToCloud(media = BytesIO(swapped_file))

            # save urls to db
            faceswap = FaceSwap.objects.create(
                source = source_face,
                target = target_face,
                swapped = swapped_face
            )

            return Response({'message': 'Images processed successfully', 'file_url': faceswap.swapped}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=400)
