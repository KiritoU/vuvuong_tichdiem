from rest_framework import pagination
from rest_framework.response import Response

from constants import constants


class CustomPagination(pagination.LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "success": 1,
                "message": constants.SUCCESS,
                "data": data,
            }
        )
