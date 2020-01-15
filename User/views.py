from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.authtoken.models import Token

from .models import User


class Register(APIView):

    permission_classes = (AllowAny,)

    # It is used for when any unknown bug or unusual situation happen in code. Then it will restrict
    # to drop the entry in db.
    # In this app I'm doing it simple since no decorators are being used.
    @transaction.atomic
    def post(self, request):
        try:
            email = request.data.get('email')
            phone_number = request.data.get('phone_number')
            password = request.data.get('password')
            confirm_password = request.data.get('confirm_password')
            first_name = request.data.get('first_name')

            if not phone_number:
                return JsonResponse({
                    'status': HTTP_400_BAD_REQUEST,
                    'message': 'Phone number required.',
                })

            if password != confirm_password:
                return JsonResponse({
                    'status': HTTP_400_BAD_REQUEST,
                    'message': 'Password not matched.',
                })

            user_email = User.objects.filter(email=email).first()
            user_phone_no = User.objects.filter(phone_number=phone_number).first()

            if user_email or user_phone_no:
                return JsonResponse({
                    'status': HTTP_400_BAD_REQUEST,
                    'message': 'Email/Phone already registered.',
                })

            with transaction.atomic():

                if not email:
                    email = None

                user = User.objects.create(
                    first_name=first_name,
                    email=email,
                    phone_number=phone_number,
                    password=make_password(password),
                    is_active=True,
                )
                user.save()

                if user:
                    token, _ = Token.objects.get_or_create(user=user)

                return JsonResponse({
                    'status': HTTP_200_OK,
                    'token': token.key,
                    'message': 'Account created.',
                })

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.info(e)
            return JsonResponse({
                'status': HTTP_400_BAD_REQUEST,
                'message': str(e),
            })
