from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

class ImageConversion :

    @staticmethod
    def copy_image(image):

        print("start copying")

        image_content = image.read()
        copy1 = BytesIO(image_content)
        copy2 = BytesIO(image_content)
        
        image_1 = InMemoryUploadedFile(copy1, 'image', image.name, image.content_type, len(image_content), None)
        image_2 = InMemoryUploadedFile(copy2, 'image', image.name, image.content_type, len(image_content), None)
        print("copied")

        return image_1, image_2
    

    @staticmethod
    def content_to_image(content):
        return InMemoryUploadedFile(BytesIO(content), 'image', 'converted_image', 'image/jpeg', len(content), None)