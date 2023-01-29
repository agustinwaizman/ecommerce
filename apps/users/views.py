from datetime import datetime
from django.contrib.sessions.models import Session
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from apps.users.authentication_mixins import Authentication
from apps.users.api.serializers import UserTokenSerializer
from apps.users.models import User


class UserToken(Authentication, APIView):
    """
    Validación de token
    """
    def get(self, request, *args, **kwargs):
        try:
            user_token = Token.objects.get_or_create(user = self.user)
            user = UserTokenSerializer(self.user)
            return Response({
                'token':user_token.key, 
                'user':user.data
                })
        except:
            return Response({'error':'credenciales invalidas'}, status=status.HTTP_400_BAD_REQUEST)


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data, context = {'request':request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token,created = Token.objects.get_or_create(user = user)
                user_serializer = UserTokenSerializer(user)
                if created:
                    return Response({
                        'token':token.key,
                        'user':user_serializer.data,
                        'message': 'Sesion iniciada.'
                    }, status=status.HTTP_201_CREATED)
                else:
                    # Para cerrar sesion en caso de un inicio en nuevo:
                    all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()
                    token.delete()
                    token = Token.objects.create(user = user)
                    return Response({
                        'token':token.key,
                        'user':user_serializer.data,
                        'message': 'Sesion iniciada.'
                    }, status=status.HTTP_201_CREATED)

                    # Para no permitir nuevos inicios de sesion:
                    # return Response({
                    #     'error': 'El usuario ya posee una sesion activa'
                    # }, status=status.HTTP_409_CONFLICT)
            else:
                return Response({'error': 'Este usuario fue desactivado'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error':'Nombre de usuario o contraseña invalidos.'}, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):

    def post(self, request, *args, **kwargs):
        try:
            token = request.GET.get('token')
            token = Token.objects.filter(key = token).first()
            if token:
                user = token.user

                all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()

                token.delete()

                session_message = 'Sesiones del usuario eliminadas'
                token_message = 'Token eliminado.'
                return Response({'token_message': token_message, 'session_message':session_message}, status=status.HTTP_200_OK)
            
            return Response({'error':'No se ha encontrado un usuario con esas credenciales'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error':'no se han enviado los parametros necesarios'}, status=status.HTTP_409_CONFLICT)