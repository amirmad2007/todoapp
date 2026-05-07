from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsNotAuthenticated
from ...models import Profile, MyUser as User
from templated_email import send_templated_mail


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    this is ia view to create JWT tokens
    """

    serializer_class = CustomTokenObtainPairSerializer


class CustomObtainToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user_id": user.id,
                "email": user.email,
                "username": user.username,
            }
        )


class DelteAuthTokenApiView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        request.user.auth_token.delete()

        return Response({"details": "TOken removed"}, status=status.HTTP_204_NO_CONTENT)


class RegisterApiView(GenericAPIView):

    permission_classes = [IsNotAuthenticated]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        email = serializer.validated_data.get("email")
        user = User.objects.get(email=email)
        token = self.get_token_for_user(user)
        access_token = token["access_token"]
        send_templated_mail(
            template_name="test-email",
            from_email="noreply@example.com",
            recipient_list=[user.email],
            context={
                "user": user,
                "site_name": "localhost",
                "access_token": access_token,
            },
        )
        username = serializer.validated_data["username"]

        return Response(
            {
                "details": (
                    f"{username} is created and we sent a email "
                    f"to {email} you need to verify to have full access to our site"
                )
            },
            status=status.HTTP_201_CREATED,
        )

    def get_token_for_user(self, user):

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return {"access_token": access_token}


class ProfileApiView(RetrieveUpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):

        return Profile.objects.get(user=self.request.user)


class ChangePasswordApiView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        return Response({"details": "password updated."}, status=status.HTTP_200_OK)


class VerifyApiView(APIView):

    permission_classes = [IsNotAuthenticated]

    def get(self, request, token, *args, **kwargs):

        try:
            accesstoken = AccessToken(token)
            user_id = accesstoken["user_id"]
            user = User.objects.get(pk=user_id)

            user.is_verified = True
            user.save()

            return Response(
                {"details": "Email verified successfully"}, status=status.HTTP_200_OK
            )

        except (TokenError, InvalidToken):
            return Response(
                {"details": "token is invalid or expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResendVerificationApiView(GenericAPIView):
    permission_classes = [IsNotAuthenticated]
    serializer_class = SendEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")

        token = self.get_token_for_user(user)
        access_token = token["access_token"]

        send_templated_mail(
            template_name="test-email",
            from_email="noreply@example.com",
            recipient_list=[user.email],
            context={
                "user": user,
                "site_name": "localhost",
                "access_token": access_token,
            },
        )
        return Response(
            {"details": f" we sent a email to {user.email} to verify your account"},
            status=status.HTTP_200_OK,
        )

    def get_token_for_user(self, user):

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return {"access_token": access_token}


class RequestResetPasswordApiView(GenericAPIView):
    permission_classes = [IsNotAuthenticated]
    serializer_class = SendEmailSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")

        token = self.get_token_for_user(user)
        access_token = token["access_token"]
        send_templated_mail(
            template_name="reset-password",
            from_email="noreply@example.com",
            recipient_list=[user.email],
            context={
                "user": user,
                "site_name": "localhost",
                "access_token": access_token,
            },
        )
        return Response(
            {"details": f" we sent a email to {user.email} to reset your passwod"},
            status=status.HTTP_200_OK,
        )

    def get_token_for_user(self, user):

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return {"access_token": access_token}


class ResendPasswordApiView(GenericAPIView):
    permission_classes = [IsNotAuthenticated]
    serializer_class = ResetPasswordSerializer

    def post(self, request, token, *args, **kwargs):
        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            user = User.objects.get(pk=user_id)

            serializer = self.serializer_class(
                data=request.data, context={"user": user}
            )
            serializer.is_valid(raise_exception=True)

            return Response({"details": "password changed "}, status=status.HTTP_200_OK)

        except (InvalidToken, TokenError):

            return Response(
                {"details": "invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
