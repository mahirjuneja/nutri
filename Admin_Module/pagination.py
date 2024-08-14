from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100  # Maximum number of items per page

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            # 'next': self.get_next_link(),
            # 'previous': self.get_previous_link(),
            'results': data
        })