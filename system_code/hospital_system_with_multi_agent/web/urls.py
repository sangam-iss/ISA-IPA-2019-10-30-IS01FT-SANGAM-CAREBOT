from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^make_appointment$', views.index, name='make_appointment'),
    url(r'^change_input$', views.change_input, name='change_input'),
    url(r'^cancel_input$', views.cancel_input, name='cancel_input'),
    url(r'^add_appointment$', views.add_appointment, name='add_appointment'),
    url(r'^change_appointment$', views.change_appointment, name='change_appointment'),
    url(r'^make_change$', views.make_change, name='make_change'),
    url(r'^cancel_appointment$', views.cancel_appointment, name='cancel_appointment'),
    url(r'^make_cancel$', views.make_cancel, name='make_cancel'),
    url(r'^get_failed_appointments$', views.get_failed_appointments, name='get_failed_appointments'),
    url(r'^get_future_appointments$', views.get_future_appointments, name='get_future_appointments'),
]