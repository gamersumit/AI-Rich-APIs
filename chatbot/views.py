from openai import OpenAI
from rest_framework import generics
from rest_framework.response import Response
from django.conf import settings
# Create your views here.

class ChatView(generics.CreateAPIView):
    def post(self, request):
        try : 
            # open ai client creation
            client = OpenAI(api_key = settings.OPENAI_API_KEY)
            
            # user's question
            promt = request.data['question']

            # open ai chat response
            respone = client.completions.create(
                model= "gpt-3.5-turbo",
                prompt = prompt,
                max_tokens =128,
                temperature=0.5
            )
            
            content = response.choices[0].message.content
            return Response({'answer' : content}, status=200)

        except Exception as e:
            print("chat bot error: ", str(e))
            return Response({"error": "Something went wrong while generating the response."}, status=400)
