from django.urls import path, re_path
from . import views
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView


app_name = 'store'

urlpatterns = [


	#marktplatz
	path('', views.marktplatz_overview, name='marktplatz_overview'),
    path('marktplatz', views.marktplatz_main, name='marktplatz_main'),
    path('inserate', views.myinserate, name="myinserate"),
    path('inserate/change/<int:pk>', views.myinserate_ändern, name="myinserate_ändern"),
    path('inserate/löschen/<int:pk>', views.myinserate_löschen, name="myinserate_löschen"),
    path('inserate/wirklich/löschen/<int:pk>', views.myinserate_wirklich, name="myinserate_wirklich"),
    path('marktplatz/video/', views.marktplatz_video, name='marktplatz_video'),
    path('marktplatz/main/<str:cat>', views.marktplatz_main_category, name='marktplatz_main_category'),
    path('marktplatz/main/jobs/<str:cat>', views.marktplatz_main_jobs_category, name='marktplatz_main_jobs_category'),
    path('marktplatz/condition/<str:cond>', views.marktplatz_condition, name='marktplatz_condition'),
    path('marktplatz/inserat/erfassen', views.marktplatz_inserat_erfassen, name='marktplatz_inserat_erfassen'),
    path('marktplatz/inserat/aendern/<int:pk>', views.marktplatz_inserat_ändern, name='marktplatz_inserat_ändern'),
    path('marktplatz/inserat/zahlung/<int:pk>/<int:tid>', views.marktplatz_zahlung, name="marktplatz_zahlung"),
    path('marktplatz/inserat/summary/<int:pk>', views.marktplatz_inserat_summary, name="marktplatz_inserat_summary"),
    path('marktplatz/inserat/erfolg/<int:pk>', views.marktplatz_inserat_erfolg, name="marktplatz_inserat_erfolg"),
    path('marktplatz/inserat/details/<str:slug>', views.marktplatz_inserat_details, name="marktplatz_inserat_details"),
    

    path('cms', views.cms, name="cms"),
    path('cms/kunden', views.cms_kunden, name='cms_kunden'),
	path('cms/kunden/erfassen', views.cms_kunden_erfassen, name='cms_kunden_erfassen'),
	path('cms/kunden/firmenname/<int:user_id>', views.cms_firmenname_bearbeiten, name='cms_firmenname_bearbeiten'),
	path('cms/user', views.cms_user, name='cms_user'),

    path('cms/marktplatz', views.cms_marktplatz, name='cms_marktplatz'),
    path('cms/marktplatz/inserat/freigegeben/<int:pk>/<str:portal>', views.cms_inserat_freigeben, name="cms_inserat_freigeben"),
    path('cms/marktplatz/inserat/deaktivieren/<int:pk>/<str:portal>', views.cms_inserat_deaktivieren, name="cms_inserat_deaktivieren"),
	path('cms/marktplatz/inserat/bearbeiten/<int:pk>', views.cms_mp_bearbeiten, name="cms_mp_bearbeiten"),
	path('cms/marktplatz/inserat/löschen/<int:pk>', views.cms_mp_löschen, name="cms_mp_löschen"),

	#jobsmarktplatz
	path('marktplatz/jobinserat/details/<int:pk>/<str:slug>', views.marktplatz_jobinserat_details, name="marktplatz_jobinserat_details"),
	path('marktplatz-jobs', views.marktplatz_jobs, name='marktplatz_jobs'),
	path('marktplatz/jobinserat/erfassen', views.marktplatz_jobinserat_erfassen, name='marktplatz_jobinserat_erfassen'),
	path('marktplatz/jobinserat/summary/<int:pk>', views.marktplatz_jobinserat_summary, name="marktplatz_jobinserat_summary"),
	path('marktplatz/jobinserat/aendern/<int:pk>', views.marktplatz_jobinserat_ändern, name='marktplatz_jobinserat_ändern'),
	path('marktplatz/jobinserat/erfolg/<int:pk>', views.marktplatz_jobinserat_erfolg, name="marktplatz_jobinserat_erfolg"),

	path('searchbar', views.searchbar, name='searchbar'),
	path('kontakt', views.kontakt, name='kontakt'),
	path('einstellungen', views.einstellungen, name='einstellungen'),
	path('impressum', views.impressum, name='impressum'),
	path('cms/login_user', views.login_user, name='login_user'),
	path('cms/logout_user', views.logout_user, name='logout_user'),
	re_path(r'^robots.txt$', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots_file"),
	



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

