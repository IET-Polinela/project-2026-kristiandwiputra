from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    
    # Ganti SerializerMethodField menjadi ReadOnlyField
    # Ini akan otomatis melacak relasi 'reporter' lalu mengambil 'username'-nya
    reporter = serializers.ReadOnlyField(source='reporter.username')

    class Meta:
        model = Report
        
        fields = [
            'id', 'title', 'category', 'description', 
            'location', 'status', 'reporter', 
            'created_at', 'updated_at'
        ]
        
        # Tambahan pengaman ekstra: 
        # Mencegah user mengedit field ini secara manual lewat Postman
        read_only_fields = ['status', 'reporter']