from django.db import models

# Create your models here.
class Enquiry(models.Model):
	PROBLEM_CATEGORY_CHOICES = (
		('HW','Hardware'),
		('SW','Software'),
	)

	STATUS_CHOICES = (
		('EN','Enquired'),
		('CH','Checked'),		# This is amazing
		('RE','Repaired'),		# Changed from Update Form when Components are added and Repair Charge is added
		('CO','Completed'),		# Changed to when Final Receipt is Generated
		('RJ','Rejected'),
	)

	receiptID = models.AutoField(primary_key=True)
	enquiryDate = models.DateField()

	customerName = models.CharField(max_length = 50)
	contactNo = models.CharField(max_length = 20)
	email = models.CharField(max_length = 50, blank=True)
	address = models.TextField(blank=True)

	deviceType = models.CharField(max_length = 50)
	brand = models.CharField(max_length = 50, blank=True)
	deviceModel = models.CharField(max_length = 50)
	serialNo = models.CharField(max_length = 50, blank=True)

	problemCategory = models.CharField(max_length = 3, choices = PROBLEM_CATEGORY_CHOICES)
	problem = models.CharField(max_length = 50)
	problemDescription = models.TextField(blank=True)

	deviceCondition = models.TextField(blank=True)

	estimatedCost = models.IntegerField()
	advance = models.IntegerField(default=0)

	status = models.CharField(max_length=3, choices = STATUS_CHOICES, default='EN')

	def __str__(self):
		return str(self.receiptID) + " : "  + self.status + " : "  + self.customerName + " : " + self.brand + " " + self.deviceModel

class TestDetail(models.Model):
	Enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE)
	actualProblem = models.CharField(max_length = 50)
	actualProblemDescription = models.TextField(blank=True)

	def __str__(self):
		return str(self.Enquiry.receiptID) + " : " + str(self.Enquiry.status) + " : " + self.Enquiry.customerName + " : " + self.actualProblem

class RepairDetail(models.Model):
	Enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE)
	componentsUsed = models.TextField(blank=True)
	repairCharge = models.IntegerField(blank=True)
	otherCharge = models.IntegerField(blank=True)
	totalPrice = models.IntegerField(blank=True)

	def __str__(self):
		return str(self.Enquiry.receiptID) + " : " + str(self.Enquiry.status) + " : " + self.Enquiry.customerName + " : " + str(self.totalPrice)

class trialPeriod(models.Model):
	ID = models.AutoField(primary_key=True)
	counter = models.IntegerField()
	date = models.DateField()