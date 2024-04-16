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
            prompt = request.data['question']

            # setup for the system
            setup = request.data['setup']

            # open ai chat response
            response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": setup},
                            {"role": "user", "content": prompt}
                        ]
                        )

            content = response.choices[0].message.content
            return Response({'answer' : content}, status=200)

        except Exception as e:
            print("chat bot error: ", str(e))
            return Response({"error": "Something went wrong while generating the response."}, status=400)
