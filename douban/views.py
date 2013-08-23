# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import utils
import json

def fans_rank(request):
    results, update_time = utils.fans_rank()
    page_num = 10
    before_page_num = 4
    after_page_num = 4

    paginator = Paginator(results, page_num)

    try:
        page = int(request.GET.get('page', '1'))
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    if page >= after_page_num:
        page_range = paginator.page_range[page - after_page_num : page + before_page_num]
    else:
        page_range = paginator.page_range[:page + before_page_num]

    try:
        page_results = paginator.page(page)
    except (EmptyPage, InvalidPage), e:
        page_results = paginator.page(paginator.num_pages)
        print e
    return render_to_response('douban_fans_rank.html', {'title': '增粉排行榜', 'fans': page_results, 'page_range': page_range, 'data': json.dumps(page_results.object_list), 'update_time': update_time.strftime('%Y/%m/%d')})