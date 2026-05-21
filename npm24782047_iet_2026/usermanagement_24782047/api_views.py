from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from .models import CustomUser

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    # Pintu gerbang dibuka untuk umum (anonim) agar bisa mendaftar
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer