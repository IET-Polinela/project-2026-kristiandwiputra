from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    # write_only=True memastikan password tidak akan pernah dimunculkan di response API
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password'] # Tambahkan field lain jika ada di CustomUser

    def create(self, validated_data):
        # Gunakan create_user agar password otomatis di-hash (dienkripsi)
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user