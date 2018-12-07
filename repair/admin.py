from django.contrib import admin

from repair.models import Enquiry,TestDetail,RepairDetail,trialPeriod

# Register your models here.

admin.site.register(Enquiry)
admin.site.register(TestDetail)
admin.site.register(RepairDetail)
admin.site.register(trialPeriod)