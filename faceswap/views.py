import base64
from io import BytesIO
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from faceswap.models import FaceSwap
from faceswap.serializers import FaceSwapSerializer
from faceswap.service import InsightFaceService
from utils.cloudinary import Cloudinary 
from django.core.files.uploadedfile import InMemoryUploadedFile

from utils.image_conversion import ImageConversion

class FaceSwapperAPIView(APIView):
   def post(self, request):
        try :
            source_img = request.FILES.get('source') # full image
            target_img = request.FILES.get('target')  # face image results    

            print("fetched data")
            source1, source2 = ImageConversion.copy_image(image=source_img)
            target1, target2 = ImageConversion.copy_image(image=target_img)


            print("duplicate images")
            swap = InsightFaceService()
            swapped_content = swap.start_swap(source = source1, target = target1)

            print("converted to base 64")
            swapped_img = ImageConversion.content_to_image(content=swapped_content)    

            print("tyep =====>", type(swapped_content))
            print("##############################")
            # save urls to db
            data = {
                'source' : source2,
                'target' : target2,
                'swapped' : swapped_img
            }

            print("data ========>", data)
            serializer = FaceSwapSerializer(data = data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print("serializer =====>", serializer.data)


            # Encode the swapped face bytes to Base64
            swapped_face_base64 = base64.b64encode(swapped_content).decode('utf-8')
            data = serializer.data
            data['swapped_hd_image'] = swapped_face_base64

            return Response({'message': 'Images processed successfully', 'data' : data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class GetSwappedImage(generics.RetrieveAPIView):
    serializer_class = FaceSwapSerializer
    queryset = FaceSwap.objects.all()