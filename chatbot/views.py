from openai import OpenAI
from rest_framework import generics
from rest_framework.response import Response
from django.conf import settings
from .serializers import PromptSerializer
# Create your views here.

class ChatView(generics.CreateAPIView):
    serializer_class = PromptSerializer
    
    def post(self, request):

        try : 
            # open ai client creation
            client = OpenAI(api_key = settings.OPENAI_API_KEY)
            print("********************************************")
            # print(request.session.session_key)
            session_key = request.session.session_key

            if not session_key:
                request.session.save()
                session_key = '843q055npcv5ky6tyjps7enq07kns3ug'
                print("not ##################333", session_key)

            print("^^^^^^^^^^^^^^", session_key)
            previous_questions = request.session.get('previous_questions', [])
            print(previous_questions) 
            # user's question
            prompt = request.data['question']
            previous_questions.append(prompt)

            chat_history = [{'role' : 'system', 'content' : 'You are a crypto encyclopedia'}]

            for question in previous_questions :
                chat_history.append({'role' : 'user', 'content' : question})

            # setup for the system
            # setup = request.data['setup']

            # open ai chat response
            response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=chat_history,
                        max_tokens=100,
                        temperature=0.7,
                        )
            # response = client.chat.completions.create(
            #             model="gpt-3.5-turbo",
            #             messages=[
            #                 {"role": "system", "content": "You are crypto encyclopedia. answer questions realted to crypto only"},
            #                 {"role": "user", "content": prompt}
            #             ]
            #             )

            content = response.choices[0].message.content
            request.session['previous_questions'] = previous_questions
            return Response({'answer' : content}, status=200)

        except Exception as e:
            print("chat bot error: ", str(e))
            return Response({"error": "Something went wrong while generating the response."}, status=400)
