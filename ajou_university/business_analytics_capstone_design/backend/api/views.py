from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from api.models import Stay, Cafe, Res, CafeTag, ResTag, CafeKwrd, ResKwrd
from api.serializers import StaySerializer, CafeSerializer, ResSerializer
from api.serializers import CafeTagSerializer, ResTagSerializer
from api.serializers import CafeKwrdSerializer, ResKwrdSerializer


# cafe
@api_view(['GET'])
def get_cafe(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    params = request.GET.getlist('tag')
    if params:
        data = CafeTag.objects.filter(tag__in=params).values_list('store_id', flat=True)
        cafe_list = Cafe.objects.filter(id__in=data).order_by('-review_count')[:30]
    else:
        cafe_list = Cafe.objects.all().order_by('-review_count')[:30]
    
    result_page = paginator.paginate_queryset(cafe_list, request)
    serializer = CafeSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

# restaurant
@api_view(['GET'])
def get_restaurant(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    params = request.GET.getlist('tag')
    if params:
        data = ResTag.objects.filter(tag__in=params).values_list('store_id', flat=True)
        res_list = Res.objects.filter(id__in=data).order_by('-review_count')[:30]
    else:
        res_list = Res.objects.all().order_by('-review_count')[:30]
    
    result_page = paginator.paginate_queryset(res_list, request)
    serializer = ResSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

# keywords
@api_view(['GET'])
def get_cafe_kwrds(request):
    data = CafeKwrd.objects.all().order_by('id')
    serializer = CafeKwrdSerializer(data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_res_kwrds(request):
    data = ResKwrd.objects.all().order_by('id')
    serializer = ResKwrdSerializer(data, many=True)
    return Response(serializer.data)

# stay
@api_view(['GET'])
def get_filter_stay(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    params = request.query_params
    district = params['district']
    data = Stay.objects.filter(district=district)
    result_page = paginator.paginate_queryset(data, request)
    serializer = StaySerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
