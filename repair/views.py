from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth import authenticate

from django.core.exceptions import ObjectDoesNotExist,  EmptyResultSet

import datetime

from repair.models import *

# Create your views here.
def dashboard(request):
	getDate = trialPeriod.objects.get(ID=1)
	if getDate.date != datetime.datetime.now().date():
		getDate.counter += 1
	getDate.save()

	if (getDate.counter > 7):
		message = {
			'errorMessage':'Trial Period Expired',
		}
		return render(request,'repair/errorPage.html', message)

	if(request.method == 'POST'):

		username = request.POST.get('username','');
		password = request.POST.get('password','');
		
		user = authenticate(username=username, password=password)
		if user is not None:
			return render(request,'repair/dashboard.html')
		else:
			message = {
				'errorMessage':'Invalid Login Credentials',
				'button':'../',
				'buttonText':'Login',
			}
			return render(request,'repair/errorPage.html', message)
	else:
		message = {
			'errorMessage':'You must login first',
			'button':'../',
			'buttonText':'Login',
		}
		return render(request,'repair/errorPage.html', message)
	

def enquiryForm(request):
	Id = Enquiry.objects.latest('receiptID')
	#Id = Enquiry.objects.earliest('receiptID')
	Id.receiptID +=1
	
	currentDate = datetime.datetime.now().date()
	currentDate = str(currentDate)
	
	return render(request,'repair/enquiryForm.html', {'receiptID': Id.receiptID, 'currentDate' : currentDate})

def enquiryReceipt(request):
	if(request.method == 'POST'):
		enquiryDate = request.POST.get('enquiryDate', datetime.datetime.now().date())
		customerName = request.POST.get('customerName','')
		contactNo = request.POST.get('contactNo','')
		email = request.POST.get('email','')
		address = request.POST.get('address','')

		deviceType = request.POST.get('deviceType','')
		brand = request.POST.get('brand','')
		deviceModel = request.POST.get('deviceModel','')
		serialNo = request.POST.get('serialNo','')
		deviceCondition = request.POST.get('deviceCondition','')

		problemCategory = request.POST.get('problemCategory','')
		problem = request.POST.get('problem','')
		problemDescription = request.POST.get('problemDescription','')

		estimatedCost = request.POST.get('estimatedCost',0)	
		advance = request.POST.get('advance',0)

		if advance == '':
			advance = 0

		enq = Enquiry(enquiryDate=enquiryDate, customerName=customerName, contactNo = contactNo, email=email, address=address, deviceType = deviceType, brand=brand, deviceModel= deviceModel, serialNo = serialNo, deviceCondition=deviceCondition,  problemCategory = problemCategory, problem = problem, problemDescription = problemDescription, estimatedCost = estimatedCost, advance = advance)
		enq.save()

		enquiryObject = Enquiry.objects.latest('receiptID')
		return render(request,'repair/enquiryReceipt.html', {'receiptID' : enquiryObject.receiptID})
	else:
		message = {
			'errorMessage':'Invalid Request',
		}
		return render(request,'repair/errorPage.html', message)

def enquiryReceiptFrameContent(request):
	if(request.method=='GET'):
			receiptID = request.GET.get('receiptID','')

			customerDetails = Enquiry.objects.filter(receiptID = receiptID)

			return render(request, 'repair/enquiryReceiptFrameContent.html', {'customerDetails' : customerDetails})
	else:
		message = {
			'errorMessage':'Invalid Request',
		}
		return render(request,'repair/errorPage.html', message)


def updateRequest(request):
	return render(request,'repair/updateRequest.html')

def updateForm(request):
	if(request.method=='POST'):
		if(request.POST.get('requestType','')=='receiptID'):
			receiptID = request.POST.get('receiptID',0)
			customerDetails = Enquiry.objects.filter(receiptID = receiptID)

			try:
				enquiryInstance = Enquiry.objects.get(receiptID = receiptID)
			except ObjectDoesNotExist:
				message = {
				'errorMessage':'No Record Exists for Receipt ID/No : ' + receiptID,
				}
				return render(request,'repair/errorPage.html', message)
		elif(request.POST.get('requestType','')=='serialNo'):
			serialNo = request.POST.get('serialNo','')

			customerDetails = Enquiry.objects.filter(serialNo = serialNo)

			try:
				enquiryInstance = Enquiry.objects.get(serialNo = serialNo)
			except ObjectDoesNotExist:
				message = {
				'errorMessage':'No Record Exists for Device Serial No. : ' + serialNo,
				}
				return render(request,'repair/errorPage.html', message)
		else:
			message = {
				'errorMessage':'Undefined Request Type',
			}
			return render(request,'repair/errorPage.html', message)

		# Add logic Here
		# Check Status
		if customerDetails[0].status == 'EN':
			data = {
				'customerDetails' : customerDetails,
			}
			return render(request, 'repair/updateForm.html', data)
		elif customerDetails[0].status == 'CH':
			testDetails = TestDetail.objects.filter(Enquiry = enquiryInstance)
			data = {
				'customerDetails' : customerDetails,
				'testDetails' : testDetails,
			}
			return render(request, 'repair/updateForm.html', data)
		elif customerDetails[0].status == 'RE' or customerDetails[0].status == 'CO':
			testDetails = TestDetail.objects.filter(Enquiry = enquiryInstance)
			repairDetails = RepairDetail.objects.filter(Enquiry = enquiryInstance)
			componentsUsed = str(repairDetails[0].componentsUsed)

			componentsUsedBackup = str(componentsUsed)
			componentsUsed = componentsUsed.split('~')
			componentsUsed = [i.split(':') for i in componentsUsed]
			del(componentsUsed[0])
			componentsUsedPriceTotal = str(sum([int(i[1]) for i in componentsUsed]))

			balance = int(repairDetails[0].totalPrice) - int(customerDetails[0].advance)

			data = {
				'customerDetails' : customerDetails,
				'testDetails' : testDetails,
				'repairDetails' : repairDetails,
				'componentsUsed' : componentsUsed,
				'componentsUsedPriceTotal' : componentsUsedPriceTotal,
				'balance' : balance,
			}
			return render(request, 'repair/updateForm.html', data)
		elif customerDetails[0].status == 'RJ':
			message = {
				'errorMessage':'This Record is Rejected',
			}
			return render(request,'repair/errorPage.html', message)
		else:
			message = {
				'errorMessage':'Your Database contains some invalid values for Enquiry.Status',
			}
			return render(request,'repair/errorPage.html', message)
	else:
		message = {
			'errorMessage':'Invalid Request',
		}
		return render(request,'repair/errorPage.html', message)

def updateTestDetails(request):
	if(request.method=='POST'):
		receiptID = request.POST.get('receiptID','')
		actualProblem = request.POST.get('actualProblem','')
		actualProblemDescription = request.POST.get('actualProblemDescription','')
		enquiryObj = Enquiry.objects.get(receiptID=receiptID)
		# Changing Status
		enquiryObj.status = 'CH'
		enquiryObj.save()
		# Updating Test Details
		testDetailsObj = TestDetail(Enquiry = enquiryObj, actualProblem = actualProblem, actualProblemDescription = actualProblemDescription)
		testDetailsObj.save()
		message = {
			'errorMessage':'Checking Details Updated Successfully',
			'button':'../',
			'buttonText':'Back',
		}
		return render(request,'repair/errorPage.html', message)
	else:
		message = {
			'errorMessage':'Invalid Request',
			'button':'../',
			'buttonText':'Back',
		}
		return render(request,'repair/errorPage.html', message)

def updateRepairDetails(request):
	if(request.method=='POST'):
		receiptID = request.POST.get('receiptID','')
		componentsUsed = request.POST.get('componentsUsed','')
		repairCharge = request.POST.get('repairCharge',0)
		otherCharge = request.POST.get('otherCharge',0)
		
		if repairCharge == '':
			repairCharge = 0

		if otherCharge == '':
			otherCharge = 0

		# Changing Status
		enquiryObj = Enquiry.objects.get(receiptID=receiptID)
		enquiryObj.status = 'RE'
		enquiryObj.save()


		if (componentsUsed != ''):
			componentsUsedBackup = str(componentsUsed)
			componentsUsed = componentsUsed.split('~')
			componentsUsed = [i.split(':') for i in componentsUsed]
			del(componentsUsed[0])
			componentsUsedPrice = [int(i[1]) for i in componentsUsed]

			totalPrice = sum(componentsUsedPrice) + int(repairCharge) + int(otherCharge)

			componentsUsed = str(componentsUsedBackup)
		else:
			totalPrice = int(repairCharge) + int(otherCharge)

		# Updating Repair Details
		repairDetailsObj = RepairDetail(Enquiry = enquiryObj, componentsUsed = componentsUsed, repairCharge = repairCharge, otherCharge = otherCharge, totalPrice = totalPrice)
		repairDetailsObj.save()

		message = {
			'errorMessage':'Repair Details Updated Successfully',
			'button': '../finalReceipt?&receiptID='+ receiptID,
			'buttonText':'Generate Final Bill',
		}
		return render(request,'repair/errorPage.html', message)
	else:
		message = {
			'errorMessage':'Invalid Request',
			'button':'../',
			'buttonText':'Back',
		}
		return render(request,'repair/errorPage.html', message)

def finalReceipt(request):
	if(request.method=='GET'):
		receiptID = request.GET.get('receiptID','')

		# Changing Status
		enquiryObj = Enquiry.objects.get(receiptID=receiptID)
		enquiryObj.status = 'CO'
		enquiryObj.save()

		data = {
			'receiptID' : receiptID,
		}
		return render(request, 'repair/finalReceipt.html', data)
	else:
		message = {
			'errorMessage':'Invalid Request',
		}
		return render(request,'repair/errorPage.html', message)
def finalReceiptFrameContent(request):
	if(request.method=='GET'):
		receiptID = request.GET.get('receiptID','')
		customerDetails = Enquiry.objects.filter(receiptID = receiptID)
		enquiryInstance = Enquiry.objects.get(receiptID = receiptID)

		testDetails = TestDetail.objects.filter(Enquiry = enquiryInstance)
		repairDetails = RepairDetail.objects.filter(Enquiry = enquiryInstance)

		componentsUsed = str(repairDetails[0].componentsUsed)

		componentsUsedBackup = str(componentsUsed)
		componentsUsed = componentsUsed.split('~')
		componentsUsed = [i.split(':') for i in componentsUsed]
		del(componentsUsed[0])
		componentsUsedPriceTotal = str(sum([int(i[1]) for i in componentsUsed]))

		balance = int(repairDetails[0].totalPrice) - int(customerDetails[0].advance)

		data = {
			'customerDetails' : customerDetails,
			'testDetails' : testDetails,
			'repairDetails' : repairDetails,
			'componentsUsed' : componentsUsed,
			'componentsUsedPriceTotal' : componentsUsedPriceTotal,
			'balance' : balance,
		}
		return render(request, 'repair/finalReceiptFrameContent.html', data)
	else:
		message = {
			'errorMessage':'Invalid Request',
		}
		return render(request,'repair/errorPage.html', message)


def pendingRepairRequest(request):
	today = datetime.date.today()
	weekAgo = today - datetime.timedelta(days=7)
	monthAgo = today - datetime.timedelta(days=30)
	today, weekAgo, monthAgo = str(today), str(weekAgo), str(monthAgo)
	dates = {
		'today' : today,
		'weekAgo' : weekAgo,
		'monthAgo' : monthAgo,
	}
	return render(request,'repair/pendingRepairRequest.html', dates)

def pendingRepairList(request):
	if(request.method=='POST'):
		dateFrom = request.POST.get('dateFrom','')
		dateTo = request.POST.get('dateTo','')
		#Sample.objects.filter(date__year='2011', date__month='01')
		pendingRepairs = Enquiry.objects.filter(enquiryDate__range = [dateFrom, dateTo], status = 'EN')
		return render(request, 'repair/pendingRepairList.html', {'pendingRepairs' : pendingRepairs})
	else:
		message = {
			'errorMessage':'Invalid Request',
		}
		return render(request,'repair/errorPage.html', message)

def checkStatusRequest(request):
	return render(request,'repair/checkStatusRequest.html')

def checkStatusShow(request):
	if(request.method=='POST'):
		if(request.POST['requestType']=='receiptID'):
			receiptID = request.POST.get('receiptID','')

			customerDetails = Enquiry.objects.filter(receiptID = receiptID)

			try:
				enquiryInstance = Enquiry.objects.get(receiptID = receiptID)
			except ObjectDoesNotExist:
				message = {
				'errorMessage':'No Record Exists for Receipt ID/No : ' + receiptID,
				}
				return render(request,'repair/errorPage.html', message)
		elif(request.POST.get('requestType','')=='serialNo'):
			serialNo = request.POST.get('serialNo','')
			
			customerDetails = Enquiry.objects.filter(serialNo = serialNo)
			
			try :
				enquiryInstance = Enquiry.objects.get(serialNo = serialNo)
			except ObjectDoesNotExist:
				message = {
				'errorMessage':'No Record Exists for Device Serial No : ' + serialNo,
				}
				return render(request,'repair/errorPage.html', message)
			
		elif(request.POST.get('requestType','')=='personalDetails'):
			customerName = request.POST.get('customerName','')
			contactNo = request.POST.get('contactNo','')
			
			customerDetails = Enquiry.objects.filter(contactNo = contactNo).filter(customerName = customerName)

			try:
				enquiryInstance = Enquiry.objects.get(contactNo = contactNo, customerName = customerName)
			except ObjectDoesNotExist:
				message = {
				'errorMessage':'No Record Exists for Customer : ' + customerName + " with Contact No " + contactNo,
				}
				return render(request,'repair/errorPage.html', message)

		else:
			message = {
				'errorMessage':'Invalid Request Type',
			}
			return render(request,'repair/errorPage.html', message)
		
		# Check Status
		if customerDetails[0].status == 'EN':
			data = {
				'customerDetails' : customerDetails,
			}
			return render(request, 'repair/checkStatusShow.html', data)
		elif customerDetails[0].status == 'CH':
			testDetails = TestDetail.objects.filter(Enquiry = enquiryInstance)
			data = {
				'customerDetails' : customerDetails,
				'testDetails' : testDetails,
			}
			return render(request, 'repair/checkStatusShow.html', data)
		elif customerDetails[0].status == 'RE' or customerDetails[0].status == 'CO':
			testDetails = TestDetail.objects.filter(Enquiry = enquiryInstance)
			repairDetails = RepairDetail.objects.filter(Enquiry = enquiryInstance)
			componentsUsed = str(repairDetails[0].componentsUsed)

			componentsUsedBackup = str(componentsUsed)
			componentsUsed = componentsUsed.split('~')
			componentsUsed = [i.split(':') for i in componentsUsed]
			del(componentsUsed[0])
			componentsUsedPriceTotal = str(sum([int(i[1]) for i in componentsUsed]))

			balance = int(repairDetails[0].totalPrice) - int(customerDetails[0].advance)

			data = {
				'customerDetails' : customerDetails,
				'testDetails' : testDetails,
				'repairDetails' : repairDetails,
				'componentsUsed' : componentsUsed,
				'componentsUsedPriceTotal' : componentsUsedPriceTotal,
				'balance' : balance,
			}
			return render(request, 'repair/checkStatusShow.html', data)
		elif customerDetails[0].status == 'RJ':
			message = {
				'errorMessage':'This Record is Rejected',
			}
			return render(request,'repair/errorPage.html', message)
		else:
			message = {
				'errorMessage':'Your Database contains some invalid values for Enquiry.Status',
			}
			return render(request,'repair/errorPage.html', message)
	else:
		message = {
			'errorMessage':'Invalid Request',
		}
		return render(request,'repair/errorPage.html', message)