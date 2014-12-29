from django.conf.urls import patterns, url

urlpatterns = patterns(
    'customforms.views',
    url(r'^form/(?P<formid>.+?)/$', 'view_form', name="view_form"),
)
