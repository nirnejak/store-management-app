from django.conf.urls import url

from .views import *

urlpatterns = [
	url(r'^$', dashboard),
	url(r'^enquiryForm/', enquiryForm),
	url(r'^enquiryReceipt/', enquiryReceipt),
	url(r'^enquiryReceiptFrameContent/',enquiryReceiptFrameContent),
	url(r'^updateRequest/', updateRequest),
	url(r'^updateForm/', updateForm),
	url(r'^updateTestDetails/',updateTestDetails),
	url(r'^updateRepairDetails/',updateRepairDetails),
	url(r'^finalReceipt/', finalReceipt),
	url(r'^finalReceiptFrameContent/',finalReceiptFrameContent),
	url(r'^pendingRepairRequest/', pendingRepairRequest),
	url(r'^pendingRepairList/', pendingRepairList),
	url(r'^checkStatusRequest/', checkStatusRequest),
	url(r'^checkStatusShow/', checkStatusShow),
]