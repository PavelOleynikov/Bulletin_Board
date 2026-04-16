from rest_framework.pagination import PageNumberPagination


class AdPagination(PageNumberPagination):
    """Пагинация для объявлений: 4 объявления на странице"""

    page_size = 4
    page_size_query_param = "page_size"
    max_page_size = 20
    page_query_param = "page"
