from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from repair.models import Enquiry

# Create your views here.

def homepage(request):
	return render(request,'index.html')
	#monospace