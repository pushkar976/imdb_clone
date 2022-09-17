from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class MovieListPagination(PageNumberPagination):
    page_size = 2                        #fetch 2 items in one page
    page_size_query_param = 'page_size'  #enable clients to fetch as many items they want by adding page_size=count
    max_page_size = 3                    #restricts the page with maximum items
    last_page_strings = 'end'        #gets the item in the last page (page=end)

class MovieLOpagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 3
    offset_query_param = 'start'