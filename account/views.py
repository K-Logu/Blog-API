from django.shortcuts import render
from .serializers import RegisterSerializer,LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#code for user registration
class ResgisterView(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = RegisterSerializer(data = data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'data': serializer.data,
                    'message': 'Account created Successfully',
                },status = status.HTTP_201_CREATED)
            
            return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong',
                },status = status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                    'data': {},
                    'message': 'Something went wrong',
                },status = status.HTTP_400_BAD_REQUEST)
 
#code for user login       
class LoginView(APIView):
    def post(self,request):
        try:
            data = request.data 
            serializer = LoginSerializer(data = data)
             
            if serializer.is_valid():
                response = serializer.get_jwt_token(serializer.data)
                return Response(response,status = status.HTTP_200_OK)
            
            return Response({
                'data': serializer.errors,
                'message': 'Somthing went wrong',
            },status = status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                'data': {},
                'message': 'Somthing went wrong',
            },status = status.HTTP_400_BAD_REQUEST)






            

        


