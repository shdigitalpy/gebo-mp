from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _


admin.site.register(Address)
admin.site.register(Kunde)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(ShippingAddress)
admin.site.register(Marketplace)
admin.site.register(MP_Category)
admin.site.register(MP_JobsCategory)
admin.site.register(JobsMarketplace)

admin.site.site_header = 'Bonetta Marktplatz'                    # default: "Django Administration"
admin.site.index_title = 'Übersicht Module'                 # default: "Site administration"
admin.site.site_title = 'Django Seitenadministration' # default: "Django site admin"
