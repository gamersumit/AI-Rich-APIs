from openai import OpenAI
from rest_framework import generics
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import render
# Create your views here.


def index_view(request):
    return render(request, 'index.html')
class ChatBotView(generics.CreateAPIView):
    
    def post(self, request):
    
        try : 
            # open ai client creation
            api_key= os.getenv( 'OPENAI_API_KEY')
            client = OpenAI(api_key = api_key)
            print("********************************************")
            session_key = request.session.session_key


            # Session Creation
            if not session_key:
                request.session.save()
                session_key = request.session.session_key
                print("not ##################333", session_key)
            print("session-key", session_key)
            
            
            # Initialized list which appends the questions asked for a session
            previous_questions = request.session.get('previous_questions', [])
            print(previous_questions)
            # Appending user's question questions list
            prompt = request.data['question']
            previous_questions.append(prompt)

            # Custom prompting of system and user
            chat_history= [
                {
            "role": "system",
            "content": f"""
            !IMPORTANT Please follow these steps:
            1. You are Crypto Assistant: It answers all the questions realted to crypto only , nothing else.Strictly,It only answer question other than crypto, if a question for information purpose is asked.
            """
            },
                {
                    "role": "system",
                    "content": f"""
                    !IMPORTANT Please follow these steps one by one:
                    1. Your purpose is to analyze {previous_questions}. If you find anything only related to "what services you provide" , respond with "BOOK AN APPOINTMENT. Type: "Confirm My Appointment" TO CONFIRM YOUR APPOINTMENT AND SEE FOR AVAILABLE SLOTS".Otherwise be crypto assistant.
                    2. After first step , analyze {previous_questions}. If you find the exact words "Confirm My Appointment". Respond with Message "Available Slots will be shown. Enter Details in the same format: title: "your_event_title", length of event:"35".Otherwise be crypto assistant.
                    3. After second step, You  purpose is to  analyze {previous_questions}. If you find user input in or related format "title: "your_event_title", length of event: "35"" then strictly respond with Message :"Success" along with convert Data in json format having all the information. Otherwise be crypto assistant.
                    4.
                    """
                },
               ]
            for question in previous_questions :
                chat_history.append({'role' : 'user', 'content' : question})

            
            # open ai chat response
            response = client.chat.completions.create(
                        model="gpt-4-turbo",
                        messages=chat_history,
                        max_tokens=100,
                        temperature=0.7,
                        )

            content = response.choices[0].message.content
            print(type(content))
            print(content)
            print(request.path,"path here")
            
            # Calling create_event API based on content recieved
            if "Success" in content:
                # Extracting JSON content from the response
                json_start_index = content.find('```json\n')
                if json_start_index != -1:
                    json_start_index += len('```json\n')
                    json_end_index = content.find('```', json_start_index)
                    if json_end_index != -1:
                        json_content = content[json_start_index:json_end_index]
                        json_data = json.loads(json_content)
                        print("json converted")
                        print(json_data)
                        print(type(json_data))

                        # Calling create_event API based on content received
                        print("******")
                        
                        # Establish a connection to the server

                        # cal_api_key= os.getenv('CAL_API_KEY')
                        reqUrl = f"https://api.cal.com/v1/event-types?apiKey=cal_live_8e81f4c669a52ae5494c746e188e4f4a"

                        headersList = {
                        "Content-Type": "application/json" ,
                        }

                        payload = json.dumps(
                        {
                            "title": json_data.get('title', ''),
                            "slug": json_data.get('title', '').lower().replace(' ', '-'),
                            "length": int(json_data.get('length of event', '10')),
                            "metadata":{}
                        })

                        response = requests.request("POST", reqUrl, data=payload,  headers=headersList)

                        print(response.text)
                        response_object = json.loads(response.text)
                        # Extract the ID from the event_type object
                        event_type_id = response_object['event_type']['id']
                        
                        print(event_type_id)
                        start_time= "2024-04-25T10:30:00.000Z"
                        booking(event_type_id, start_time)
                        if response.status_code == 200:
                            # Return success response
                            print("successfully created event")
                        else:
                            # Return error response
                            print("failed to create event")
                        
                        
            request.session['previous_questions'] = previous_questions
            # template_data = {'answer': content}
            # return render(request, 'chatbot.html', template_data)
            return Response(content, status=200)

        except Exception as e:
            print("chat bot error: ", str(e))
            return Response({"error": "Something went wrong while generating the response."}, status=400)


# booking function to add event to calender
def booking(event_id, start_time):
    # cal_api_key= os.getenv('CAL_API_KEY')
    reqUrl = "https://api.cal.com/v1/bookings?apiKey=cal_live_8e81f4c669a52ae5494c746e188e4f4a"
    
    print('11')

    headersList = {
     "Content-Type": "application/json" 
    }

    payload = json.dumps(
    {
      
        "eventTypeId": event_id,
        "start": start_time,
        "end": "2024-04-25T10:40:00.000Z",
        "responses": {
          "name": "Lalit Kumar Yadav",
          "email": "lalit@snakescript.com",
          "location": "Calcom HQ"
        },
        "timeZone": "Asia/Calcutta",
        "language": "en",
        "metadata":{}
      
    })
    print('22')
    response = requests.request("POST", reqUrl, data=payload,  headers=headersList)
    print(response.text)
    if response.status_code == 200:
                            # Return success response
        print("successfully booked")
    else:
        # Return error response
        print("failed to book")

    # print(response.text)
