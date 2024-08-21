from django.shortcuts import render
from .models import person,Login
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password,check_password
import json
from datetime import datetime
import pytz
import smtplib
from django.core.mail import send_mail
from django.conf import settings
import random
from django.views.decorators.csrf import csrf_exempt

from .Queries import handlequery, serialize_mongo_documents





def index(request):
  return render(request,'index.html')

@api_view(['POST'])
def add(request):
  # data = request.data
  data = json.loads(request.body)
  name=data['username']
  email=data['email']
  

  def is_valid_email_domain(email):
    # Extract domain from email address
    domain = email.split('@')[-1]

    # List of known valid domains
    valid_domains = [  'gmail.com',
    'yahoo.com',
    'hotmail.com',
    'outlook.com',
    'icloud.com',
    'mail.com',
    'zoho.com',
    'inbox.com',
    'live.com',
    'fastmail.com','gmail.co.uk',
    'hotmail.co.uk',
    'yahoo.co.uk',
    'sky.com','hotmail.fr','yahoo.co.jp',
    'hotmail.co.jp',
    'docomo.ne.jp','yahoo.com.au','yahoo.de',
    'hotmail.de','yahoo.co.za','hotmail.com.br',
    'gmail.com.br',
    'yahoo.com.br','yahoo.it',
    'hotmail.it','vodafone.it',
    'yahoo.com.mx',
    'hotmail.com.mx','gmail.com.mx',
    'yahoo.com.ar',
    'hotmail.com.ar',
    'live.com.ar', 'hotmail.com.co',
    'yahoo.com.co',
    'gmail.com.co',
    'outlook.com.co',
    'hotmail.es',
    'yahoo.es',
    'gmail.es','mail.com',
    'email.com','googlemail.com',
    'outlook.com',
    'live.com','office365.com',
    'outlook.co.uk', 'yahoo.com.ua',
    'yahoo.com.ru',
    'yahoo.com.cn',
    'yahoo.co.uk','yahoo.co.in','facebook.com',
    'twitter.com','instagram.com','x.com','whatsapp.com']  # Add more valid domains as needed

    # Check if the domain is in the list of valid domains
    return domain in valid_domains

# Example usage:


  if is_valid_email_domain(email)==False:
    message=f'Email was wrong, {name} could not Sign Up'
    
    return JsonResponse({"status": "unsuccessful", "message": "Wrong Email"})


  
  user = person.find_one({"username": name})
  
  if user:
     message=f'Person with same username already exists, {name} could not Sign Up'
     
     return JsonResponse({"status": "unsuccessful", "message": "A person with same username already exists"})
  hashed_password = make_password(data['password'])
  
  utc_now = datetime.now(pytz.utc)

# Define the IST timezone
  ist_timezone = pytz.timezone('Asia/Kolkata')

# Convert the current time to IST
  ist_now = utc_now.astimezone(ist_timezone)

# Extract date and time separately
  current_date_ist = ist_now.date()
  current_time_ist = ist_now.time()
  current_date=current_date_ist.strftime('%Y-%m-%d')
  current_time=current_time_ist.strftime('%H:%M:%S')

  records={
     "username":data['username'],
    "firstname": data['firstName'],
    "lastname": data['lastName'],
    "country":data['country'],
    "Security Question":data['select'],
    "Answer":data['ans'],
    "email":data['email'],
    "password1":hashed_password,
    "password2":"",
    "password3":"",
    "Date":current_date,
    "Time":current_time,
  }
  # username=user['username']
  message=f'{name} Signed Up'
 
  person.insert_one(records)
  return HttpResponse("Yes")

@api_view(['POST'])
def login(request):
  # data = request.data
  data = json.loads(request.body)
  name=data['username']
  password=data['password']
  
  user = person.find_one({"username": name})
 
 
  utc_now = datetime.now(pytz.utc)

# Define the IST timezone
  ist_timezone = pytz.timezone('Asia/Kolkata')

# Convert the current time to IST
  ist_now = utc_now.astimezone(ist_timezone)

# Extract date and time separately
  current_date_ist = ist_now.date()
  current_time_ist = ist_now.time()
  current_date=current_date_ist.strftime('%Y-%m-%d')
  current_time=current_time_ist.strftime('%H:%M:%S')
  

  if user:
    if check_password(password, user['password1']):
     
     records={
                "username":name,
                "Date":current_date,
                "Time":current_time,
                "Status":"Logged-In"
                }

     message=f'{name} Logged-In at {current_time} IST '

       
            
  
     Login.insert_one(records)
     return JsonResponse({"status": "success", "message": "Logged in successfully"})
    else:
        records={
                "username":name,
                "Date":current_date,
                "Time":current_time,
                "Status":"Login Failed"
                }
        message=f'{name} Login failed at {current_time} IST '
        
        # with open("../log.txt","a") as file:
        #    file.write("Login failed")                    
        Login.insert_one(records)
        return JsonResponse({"status": "error", "message": "Wrong password"})
  else:
        return JsonResponse({"status": "error", "message": "Username does not exist"})
   

  # person.insert_one(records)
@csrf_exempt
@api_view(['POST'])
def otp(request):
  data = json.loads(request.body)
  
  def generate_otp():
    # Generate a 6-digit OTP (can be customized)
    return str(random.randint(100000, 999999))
  otp=generate_otp()

  original_starttls = smtplib.SMTP.starttls

  def debug_starttls(self, *args, **kwargs):
    print(f'starttls called with args: {args}, kwargs: {kwargs}')
    # Remove unexpected keyword arguments
    kwargs.pop('keyfile', None)
    kwargs.pop('certfile', None)
    return original_starttls(self, *args, **kwargs)

  smtplib.SMTP.starttls = debug_starttls


  subject = 'Your OTP for Login'
  message = f'Your OTP is: {otp}. This OTP is valid for 5 minutes.'
  from_email = settings.EMAIL_HOST_USER
  em=data['username']
  em1=data['email']
  recipient_list = [em1]
  user = person.find_one({"username": em})
  if user:
     if  user['email']==em1:
        send_mail(subject, message, from_email, recipient_list,fail_silently=False)
        message=f'OTP sent to {em1}'
        
        return JsonResponse({"status": "success", "message": "Otp Sent","otp_to_check":otp})
     else:
      
      return JsonResponse({"status": "unsuccessful", "message": "Email not registered.","otp_to_check":otp})
  else:
       
       return JsonResponse({"status": "unsuccessful", "message": "Username not present.","otp_to_check":otp})
  
     
  

@api_view(['POST'])
def otpverify(request):
  data = json.loads(request.body)
  
  user_otp=data['otp']
  otp=data['otp_to']
  if(otp==user_otp):
    
    return JsonResponse({"status": "success", "message": "Otp matched"})
  
  else:
     
     return JsonResponse({"status": "unsuccessful", "message": "Otp did not match"})
  
@api_view(['POST'])
def newpass(request):
  data = json.loads(request.body)
  
  us=data['username']
 
  password=data['passw']
  hashed_password=make_password(password)
  user = person.find_one({"username": us})
  
  if user:
    if check_password(password, user['password1']) or check_password(password, user['password2']) or check_password(password, user['password3']):
        
        return JsonResponse({"status": "unsuccessful", "message": "Password cannot be the same as previous passwords"})
    elif(user['password2']==""):
       message=f'Password changed for {us}'
       
       passworda=user['password1']
       person.update_one(
          {"username": us},
          {
        "$set": {
            "password1": hashed_password,
            "password2": passworda
        }
    } )
       return JsonResponse({"status": "success", "message": "Password changed"})
    elif(user['password3']==""):
       message=f'Password changed for {us}'
       
       passworda=user['password1']
       passwordb=user['password2']
       person.update_one(
          {"username": us},
          {
        "$set": {
            "password1": hashed_password,
            "password2": passworda,
            "password3": passwordb
        }
    }
          )
       return JsonResponse({"status": "success", "message": "Password changed"})
    else:
       message=f'Password changed for {us}'
      
       passworda=user['password1']
       passwordb=user['password2']
       person.update_one(
          {"username": us},
          {"$set": {
            "password1": hashed_password,
            "password2": passworda,
            "password3": passwordb
        }}
          )
       return JsonResponse({"status": "success", "message": "Password Changed"})
  
  
@api_view(['POST'])
def logout(request):
   data = json.loads(request.body)
   name=data['username']
  
   utc_now = datetime.now(pytz.utc)

# Define the IST timezone
   ist_timezone = pytz.timezone('Asia/Kolkata')

# Convert the current time to IST
   ist_now = utc_now.astimezone(ist_timezone)

# Extract date and time separately
   current_date_ist = ist_now.date()
   current_time_ist = ist_now.time()
   current_date=current_date_ist.strftime('%Y-%m-%d')
   current_time=current_time_ist.strftime('%H:%M:%S')

   records={
      
      "username":name,
      "Date":current_date,
      "Time":current_time,
      "Status":"Logged-Out"
         }
                            
   Login.insert_one(records)
   return JsonResponse({"status": "success", "message": "Collection deleted"})

from bson import ObjectId

def serialize_mongo_documents(documents):
    serialized_docs = []
    
    if isinstance(documents, str):
        return [{"message":documents}]

    for doc in documents:
        serialized_doc = {}
        for key, value in doc.items():
            if key=="password1" or key=="password2" or key=="password3" or key=="_id":
               continue
            if isinstance(value, ObjectId):
                serialized_doc[key] = str(value)
            else:
                serialized_doc[key] = value
        serialized_docs.append(serialized_doc)
    return serialized_docs

@api_view(['POST'])
def newmessage(request):
    data = json.loads(request.body)
    name = data['username']
    newMessage = data['newChat']
    result = handlequery(newMessage)

    serialized_result = serialize_mongo_documents(result)
    return JsonResponse({"status": "Success", "result": serialized_result})





# from django.shortcuts import render
# from .models import person,Login
# from django.http import JsonResponse,HttpResponse
# from rest_framework.decorators import api_view
# from django.contrib.auth.hashers import make_password,check_password
# import json
# from datetime import datetime
# import pytz
# import smtplib
# from django.core.mail import send_mail
# from django.conf import settings
# import random
# from django.views.decorators.csrf import csrf_exempt

# from .Queries import handlequery






# def index(request):
#   return render(request,'index.html')

# @api_view(['POST'])
# def add(request):
#   # data = request.data
#   data = json.loads(request.body)
#   name=data['username']
#   email=data['email']
  

#   def is_valid_email_domain(email):
#     # Extract domain from email address
#     domain = email.split('@')[-1]

#     # List of known valid domains
#     valid_domains = [  'gmail.com',
#     'yahoo.com',
#     'hotmail.com',
#     'outlook.com',
#     'icloud.com',
#     'mail.com',
#     'zoho.com',
#     'inbox.com',
#     'live.com',
#     'fastmail.com','gmail.co.uk',
#     'hotmail.co.uk',
#     'yahoo.co.uk',
#     'sky.com','hotmail.fr','yahoo.co.jp',
#     'hotmail.co.jp',
#     'docomo.ne.jp','yahoo.com.au','yahoo.de',
#     'hotmail.de','yahoo.co.za','hotmail.com.br',
#     'gmail.com.br',
#     'yahoo.com.br','yahoo.it',
#     'hotmail.it','vodafone.it',
#     'yahoo.com.mx',
#     'hotmail.com.mx','gmail.com.mx',
#     'yahoo.com.ar',
#     'hotmail.com.ar',
#     'live.com.ar', 'hotmail.com.co',
#     'yahoo.com.co',
#     'gmail.com.co',
#     'outlook.com.co',
#     'hotmail.es',
#     'yahoo.es',
#     'gmail.es','mail.com',
#     'email.com','googlemail.com',
#     'outlook.com',
#     'live.com','office365.com',
#     'outlook.co.uk', 'yahoo.com.ua',
#     'yahoo.com.ru',
#     'yahoo.com.cn',
#     'yahoo.co.uk','yahoo.co.in','facebook.com',
#     'twitter.com','instagram.com','x.com','whatsapp.com']  # Add more valid domains as needed

#     # Check if the domain is in the list of valid domains
#     return domain in valid_domains

# # Example usage:


#   if is_valid_email_domain(email)==False:
#     message=f'Email was wrong, {name} could not Sign Up'
    
#     return JsonResponse({"status": "unsuccessful", "message": "Wrong Email"})


  
#   user = person.find_one({"username": name})
  
#   if user:
#      message=f'Person with same username already exists, {name} could not Sign Up'
     
#      return JsonResponse({"status": "unsuccessful", "message": "A person with same username already exists"})
#   hashed_password = make_password(data['password'])
  
#   utc_now = datetime.now(pytz.utc)

# # Define the IST timezone
#   ist_timezone = pytz.timezone('Asia/Kolkata')

# # Convert the current time to IST
#   ist_now = utc_now.astimezone(ist_timezone)

# # Extract date and time separately
#   current_date_ist = ist_now.date()
#   current_time_ist = ist_now.time()
#   current_date=current_date_ist.strftime('%Y-%m-%d')
#   current_time=current_time_ist.strftime('%H:%M:%S')

#   records={
#      "username":data['username'],
#     "firstname": data['firstName'],
#     "lastname": data['lastName'],
#     "country":data['country'],
#     "Security Question":data['select'],
#     "Answer":data['ans'],
#     "email":data['email'],
#     "password1":hashed_password,
#     "password2":"",
#     "password3":"",
#     "Date":current_date,
#     "Time":current_time,
#   }
#   # username=user['username']
#   message=f'{name} Signed Up'
 
#   person.insert_one(records)
#   return HttpResponse("Yes")

# @api_view(['POST'])
# def login(request):
#   # data = request.data
#   data = json.loads(request.body)
#   name=data['username']
#   password=data['password']
  
#   user = person.find_one({"username": name})
 
 
#   utc_now = datetime.now(pytz.utc)

# # Define the IST timezone
#   ist_timezone = pytz.timezone('Asia/Kolkata')

# # Convert the current time to IST
#   ist_now = utc_now.astimezone(ist_timezone)

# # Extract date and time separately
#   current_date_ist = ist_now.date()
#   current_time_ist = ist_now.time()
#   current_date=current_date_ist.strftime('%Y-%m-%d')
#   current_time=current_time_ist.strftime('%H:%M:%S')
  

#   if user:
#     if check_password(password, user['password1']):
     
#      records={
#                 "username":name,
#                 "Date":current_date,
#                 "Time":current_time,
#                 "Status":"Logged-In"
#                 }

#      message=f'{name} Logged-In at {current_time} IST '

       
            
  
#      Login.insert_one(records)
#      return JsonResponse({"status": "success", "message": "Logged in successfully"})
#     else:
#         records={
#                 "username":name,
#                 "Date":current_date,
#                 "Time":current_time,
#                 "Status":"Login Failed"
#                 }
#         message=f'{name} Login failed at {current_time} IST '
        
#         # with open("../log.txt","a") as file:
#         #    file.write("Login failed")                    
#         Login.insert_one(records)
#         return JsonResponse({"status": "error", "message": "Wrong password"})
#   else:
#         return JsonResponse({"status": "error", "message": "Username does not exist"})
   

#   # person.insert_one(records)
# @csrf_exempt
# @api_view(['POST'])
# def otp(request):
#   data = json.loads(request.body)
  
#   def generate_otp():
#     # Generate a 6-digit OTP (can be customized)
#     return str(random.randint(100000, 999999))
#   otp=generate_otp()

#   original_starttls = smtplib.SMTP.starttls

#   def debug_starttls(self, *args, **kwargs):
#     print(f'starttls called with args: {args}, kwargs: {kwargs}')
#     # Remove unexpected keyword arguments
#     kwargs.pop('keyfile', None)
#     kwargs.pop('certfile', None)
#     return original_starttls(self, *args, **kwargs)

#   smtplib.SMTP.starttls = debug_starttls


#   subject = 'Your OTP for Login'
#   message = f'Your OTP is: {otp}. This OTP is valid for 5 minutes.'
#   from_email = settings.EMAIL_HOST_USER
#   em=data['username']
#   em1=data['email']
#   recipient_list = [em1]
#   user = person.find_one({"username": em})
#   if user:
#      if  user['email']==em1:
#         send_mail(subject, message, from_email, recipient_list,fail_silently=False)
#         message=f'OTP sent to {em1}'
        
#         return JsonResponse({"status": "success", "message": "Otp Sent","otp_to_check":otp})
#      else:
      
#       return JsonResponse({"status": "unsuccessful", "message": "Email not registered.","otp_to_check":otp})
#   else:
       
#        return JsonResponse({"status": "unsuccessful", "message": "Username not present.","otp_to_check":otp})
  
     
  

# @api_view(['POST'])
# def otpverify(request):
#   data = json.loads(request.body)
  
#   user_otp=data['otp']
#   otp=data['otp_to']
#   if(otp==user_otp):
    
#     return JsonResponse({"status": "success", "message": "Otp matched"})
  
#   else:
     
#      return JsonResponse({"status": "unsuccessful", "message": "Otp did not match"})
  
# @api_view(['POST'])
# def newpass(request):
#   data = json.loads(request.body)
  
#   us=data['username']
 
#   password=data['passw']
#   hashed_password=make_password(password)
#   user = person.find_one({"username": us})
  
#   if user:
#     if check_password(password, user['password1']) or check_password(password, user['password2']) or check_password(password, user['password3']):
        
#         return JsonResponse({"status": "unsuccessful", "message": "Password cannot be the same as previous passwords"})
#     elif(user['password2']==""):
#        message=f'Password changed for {us}'
       
#        passworda=user['password1']
#        person.update_one(
#           {"username": us},
#           {
#         "$set": {
#             "password1": hashed_password,
#             "password2": passworda
#         }
#     } )
#        return JsonResponse({"status": "success", "message": "Password changed"})
#     elif(user['password3']==""):
#        message=f'Password changed for {us}'
       
#        passworda=user['password1']
#        passwordb=user['password2']
#        person.update_one(
#           {"username": us},
#           {
#         "$set": {
#             "password1": hashed_password,
#             "password2": passworda,
#             "password3": passwordb
#         }
#     }
#           )
#        return JsonResponse({"status": "success", "message": "Password changed"})
#     else:
#        message=f'Password changed for {us}'
      
#        passworda=user['password1']
#        passwordb=user['password2']
#        person.update_one(
#           {"username": us},
#           {"$set": {
#             "password1": hashed_password,
#             "password2": passworda,
#             "password3": passwordb
#         }}
#           )
#        return JsonResponse({"status": "success", "message": "Password Changed"})
  
  
# @api_view(['POST'])
# def logout(request):
#    data = json.loads(request.body)
#    name=data['username']
  
#    utc_now = datetime.now(pytz.utc)

# # Define the IST timezone
#    ist_timezone = pytz.timezone('Asia/Kolkata')

# # Convert the current time to IST
#    ist_now = utc_now.astimezone(ist_timezone)

# # Extract date and time separately
#    current_date_ist = ist_now.date()
#    current_time_ist = ist_now.time()
#    current_date=current_date_ist.strftime('%Y-%m-%d')
#    current_time=current_time_ist.strftime('%H:%M:%S')

#    records={
      
#       "username":name,
#       "Date":current_date,
#       "Time":current_time,
#       "Status":"Logged-Out"
#          }
                            
#    Login.insert_one(records)
#    return JsonResponse({"status": "success", "message": "Collection deleted"})

# from bson import ObjectId

# def serialize_mongo_documents(documents):
#     serialized_docs = []
    
#     if isinstance(documents, str):
#         return [{"message":documents}]

#     for doc in documents:
#         serialized_doc = {}
#         for key, value in doc.items():
#             if key=="password1" or key=="password2" or key=="password3" or key=="_id":
#                continue
#             if isinstance(value, ObjectId):
#                 serialized_doc[key] = str(value)
#             else:
#                 serialized_doc[key] = value
#         serialized_docs.append(serialized_doc)
#     return serialized_docs

# @api_view(['POST'])
# def newmessage(request):
#    data = json.loads(request.body)
#    name=data['username']
#    newMessage=data['newChat']
#    result=handlequery(newMessage)

#    serialized_result = serialize_mongo_documents(result)
#    return JsonResponse({"status":"Success","result":serialized_result})
