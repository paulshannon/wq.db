from django.conf.urls import patterns, include, url
from wq.db import rest
from wq.db.contrib.chart.urls import make_urls
from tests.chart_app import views

chart_urls = make_urls({
    'timeseries': views.TimeSeriesView,
    'scatter': views.ScatterView,
    'boxplot': views.BoxPlotView,
})

rest.autodiscover()
urlpatterns = patterns(
    '',
    url(r'^',       include(rest.router.urls)),
    url(r'^chart',  include(chart_urls)),
)
