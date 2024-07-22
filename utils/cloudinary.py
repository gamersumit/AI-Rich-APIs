import utils.cloudinary as cloudinary
import cloudinary.api
from cloudinary import uploader


class Cloudinary:  

    @staticmethod
    def UploadMediaToCloud(media, path = "faceswap/"):
        print("media ===>", media)
        print("media ===>", type(media))
        upload = uploader.upload_large(media, folder = path, use_filename = True)   
        print(upload)

        return upload['secure_url']
       


    @staticmethod
    def delete_media_from_cloudinary(urls):
        public_ids = [url[url.index('faceswap/'):] for url in urls]
        response = cloudinary.api.delete_resources(public_ids, resource_type = 'raw')
             
       