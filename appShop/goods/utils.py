
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from goods.models import Products


def q_serch(query):
    if query.isdigit() and len(query) <= 4:
        return Products.objects.filter(id=int(query))
    
    vector = SearchVector(SearchVector('name', 'description'))
    query = SearchQuery(query)
   
    
    return Products.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by("-rank")

    
    # keywords = [word for word in query.split() if len(word) > 2]

    # q_objects = Q()

    # for token in keywords:
    #     q_objects |= Q(description=token)
    #     q_objects |= Q(name=token)
    
    # return Products.objects.filter(q_objects)