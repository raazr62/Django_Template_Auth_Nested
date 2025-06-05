from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny


# User registration
class UserCreateView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            response = {
                "status": status.HTTP_201_CREATED,  # ✅ match real status code
                "success": True,
                "message": "User profile created successfully",
                "data": CustomUserSerializer(user).data
            }

            return Response(response, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Validation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# User list (for debugging/testing purpose)
class UserListView(APIView):
    
      permission_classes = [AllowAny]  
      def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)














# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import CustomUser
# from .serializers import CustomUserSerializer

# # for sign up only
# from rest_framework.permissions import AllowAny  


# # for sign up only
# class UserCreateView(APIView):
#     permission_classes = [AllowAny]  

#     def post(self, request):
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()

#             response = {
#                 "status" : status.HTTP_200_OK, 
#                 "success" : True,
#                 "message" : "Profile created Successfully",

#                 "data" : CustomUserSerializer(user).data
#             }

#             return Response(response, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserListView(APIView):
#     def get(self, request):
#         users = CustomUser.objects.all()
#         serializer = CustomUserSerializer(users, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)






# {
#   "email": "{{$randomEmail}}",
#   "full_name": "admin",
#   "password": "Test123!",
#   "profile": {
#     "bio": "I love coding",
#     "location": "Dhaka",
#     "phone": "0123456789",
#     "skills": ["python","django","php"],
#     "payment_method": {
#       "method_name": "MasterCard",
#       "card_number": "4242424242424242",
#       "expiry_date": "2020-06-12",
#       "cvv": "123",
#       "billing_address": "123 Main St"
#     },
#     "address": {
#       "city": "Dhaka",
#       "country": "Bangladesh",
#       "zipcode": "7867",
#       "state": "Dhaka",
#       "street":"hggjh"
#     }
#   }
# }