from django.conf.urls import patterns, url

urlpatterns = patterns('douban.views',
                       url(r'^fans_rank/$', 'fans_rank'),
                       )