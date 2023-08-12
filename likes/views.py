from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LikeSerializer
from uuid import UUID


class LikeView (APIView):

    serializer_class = LikeSerializer  # default
    permission_classes = [permissions.IsAuthenticated]
    unlike = False

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        if instance is None:
            self.unlike = True
        return Response(status=status.HTTP_200_OK)
