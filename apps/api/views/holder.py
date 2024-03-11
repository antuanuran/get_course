from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.api.serializers.holder import ImageHolderSerializer, LinkHolderSerializer, VideoHolderSerializer


@api_view(http_method_names=["post"])
@permission_classes([IsAuthenticated])
def upload_image_view(request):
    serializer = ImageHolderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    filename = serializer.validated_data.get("name", serializer.validated_data["file"].name)
    serializer.save(name=filename)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(http_method_names=["post"])
@permission_classes([IsAuthenticated])
def upload_video_view(request):
    serializer = VideoHolderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    filename = serializer.validated_data.get("name", serializer.validated_data["file"].name)
    serializer.save(name=filename)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(http_method_names=["post"])
@permission_classes([IsAuthenticated])
def upload_link_view(request):
    serializer = LinkHolderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
