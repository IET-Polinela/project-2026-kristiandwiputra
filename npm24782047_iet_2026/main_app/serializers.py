from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id',
            'title',
            'category',
            'description',
            'location',
            'status',
            'reporter',
            'is_owner',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['reporter', 'is_owner', 'created_at', 'updated_at']

    def get_is_owner(self, obj):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        return obj.reporter_id == request.user.id

    def get_reporter(self, obj):
        request = self.context.get('request')

        if not obj.reporter:
            return '-'

        if request and request.user.is_authenticated:
            is_admin_user = getattr(request.user, 'is_admin', False)

            if obj.reporter_id == request.user.id or request.user.is_superuser or is_admin_user:
                return obj.reporter.username

        return 'Warga Anonim'

    def validate_status(self, value):
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            is_admin_user = getattr(request.user, 'is_admin', False)

            if request.user.is_superuser or is_admin_user:
                return value

        if value not in ['DRAFT', 'REPORTED']:
            raise serializers.ValidationError('Citizen hanya boleh menyimpan DRAFT atau mengajukan REPORTED.')

        return value