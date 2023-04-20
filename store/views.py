from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.views.generic import ListView, DetailView, View, UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import *
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.shortcuts import reverse, HttpResponse
from django.db.models import Q, Count, Sum
from django.db.models.functions import Coalesce
from django.template.loader import render_to_string, get_template
from django.conf import settings
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required
from itertools import chain

@login_required
def marktplatz_jobinserat_erfolg(request, pk):
	mp = get_object_or_404(JobsMarketplace, id=pk)

	'''subject = 'Inserat Nr.' + ' ' + str(mp.id) + ' ' + mp.title + ' wurde erstellt.'
	if mp.condition == "G":
		condition = "Gebraucht"
	else:
		condition = "Neu"
	template = render_to_string('marktplatz/inserat-email-erfolg.html', {
			'title' : mp.title,
			'price': mp.price, 
			'condition': mp.condition,
			'place': mp.place,
			'add_date': mp.add_date,
			'category': mp.category,		
					 })
	email = ''	
	#send email for order
	email = EmailMessage(
			subject,
			template,
			email,
			['sandro@sh-digital.ch','livio.bonetta@geboshop.ch'],
				)
	email.fail_silently=False
	email.content_subtype = "html"
	email.send()'''

	context = {

	'mp' : mp,
		
				}
	return render(request, 'marktplatz/marktplatz-jobs-erfolg.html', context)


@login_required
def marktplatz_jobinserat_summary(request, pk):
	mp = get_object_or_404(JobsMarketplace, id=pk)

	if request.method == "POST":
		#return redirect(link)
		return redirect ("store:marktplatz_jobinserat_erfolg", pk=mp.id)

	else:
		context = {	
			'inserat' : mp,
				
				}
	
		return render(request, 'marktplatz/marktplatz-jobsummary.html', context)

@login_required
def marktplatz_jobinserat_ändern(request, pk):
	inserat = get_object_or_404(JobsMarketplace, id=pk)
	
	if request.method == "POST":
		form = InseratJobsCreateForm(request.POST or None, request.FILES or None, instance=inserat)
		if form.is_valid():
			mp = form.save(commit=False)
			mp.user = request.user
			mp.save()
			return redirect('store:marktplatz_jobinserat_summary', pk=mp.id)

		else:
			messages.error(request, "Error")

	else: 
		form = form = InseratJobsCreateForm(instance=inserat)

	context = {
		'form': form,
				}
	return render(request, 'marktplatz/marktplatz-inserat-erfassen.html', context)


@login_required
def marktplatz_jobinserat_erfassen(request):
	if request.method == "POST":
		form = InseratJobsCreateForm(request.POST or None,request.FILES or None,)
		if form.is_valid():
			mp = form.save(commit=False)
			mp.user = request.user
			mp.save()
			
			return redirect('store:marktplatz_jobinserat_summary', pk=mp.id)

		else:
			messages.error(request, "Error")

	else: 
		form = form = InseratJobsCreateForm()

	context = {
		'form': form,
				}
	return render(request, 'marktplatz/marktplatz-jobs-erstellen.html', context)



def marktplatz_video(request):
	context = {
	
	}
	return render (request, 'marktplatz/marktplatz-video.html', context)

def marktplatz_jobs(request):
	mp_categories = MP_JobsCategory.objects.all().order_by('name')
	search_query = request.GET.get('search', '')

	if search_query:
		mp_inserate = JobsMarketplace.objects.filter(Q(place__icontains=search_query) | Q(region__icontains=search_query))

	else:
		mp_inserate = JobsMarketplace.objects.all()


	context = {

	'mp_inserate': mp_inserate,
	'mp_categories': mp_categories,
	

	}
	return render (request, 'marktplatz/marktplatz-jobs.html', context)

def marktplatz_overview(request):
	
	context = {

			
		
				}
	return render(request, 'marktplatz/marktplatz-overview.html', context)

@login_required
def marktplatz_zahlung(request, pk, tid):
	mp = get_object_or_404(Marketplace, id=pk)
	#### regular
	context = {

			'inserat' : mp,
		
				}
	return render(request, 'marktplatz/marktplatz-zahlung.html', context)

@login_required
def marktplatz_inserat_summary(request, pk):
	import urllib.request
	import hmac
	import hashlib
	import base64
	import json

	mp = get_object_or_404(Marketplace, id=pk)

	betrag = 1500
	sku = int(mp.id) + 1000

	post_data = {
	"amount": betrag,
	"vatRate": 7.7,
	"currency": "CHF",
	"sku": sku,
	"preAuthorization": 0,
	"reservation": 0,
	"successRedirectUrl": settings.PAYMENT_SUCCESS_URL,
	"failedRedirectUrl": settings.PAYMENT_DECLINE_URL

			}

	data = urllib.parse.urlencode(post_data).encode('UTF-8')

	string = settings.INSTANCE_API_SECRET
	as_bytes = bytes(string, 'UTF-8')

	dig = hmac.new(as_bytes, msg=data, digestmod=hashlib.sha256).digest()
	post_data['ApiSignature'] = base64.b64encode(dig).decode()
	post_data['instance'] = settings.INSTANCE_NAME

	data = urllib.parse.urlencode(post_data, quote_via=urllib.parse.quote).encode('UTF-8')

	try:
		payment_url = settings.PAYMENT_URL_OPEN

		url = urllib.request.urlopen(payment_url, data) 
		
		content = url.read().decode('UTF-8')
		response = json.loads(content)
		result = response['data'][0]['id']
		link = response['data'][0]['link']

	except Exception as exc:
		result = "Wrong"

	mp.tid = result
	mp.save()

	if request.method == "POST":
		#return redirect(link)
		return redirect ("store:marktplatz_inserat_erfolg", pk=mp.id)

	else:
		context = {	
			'inserat' : mp,
			'result' : result,
			'tid' : result,
		
				}
	
		return render(request, 'marktplatz/marktplatz-summary.html', context)

@login_required
def marktplatz_inserat_erfolg(request, pk):
	mp = get_object_or_404(Marketplace, id=pk)

	subject = 'Inserat Nr.' + ' ' + str(mp.id) + ' ' + mp.title + ' wurde erstellt.'
	if mp.condition == "G":
		condition = "Gebraucht"
	else:
		condition = "Neu"
	template = render_to_string('marktplatz/inserat-email-erfolg.html', {
			'title' : mp.title,
			'price': mp.price, 
			'condition': mp.condition,
			'place': mp.place,
			'add_date': mp.add_date,
			'category': mp.category,		
					 })
	email = ''	
	#send email for order
	email = EmailMessage(
			subject,
			template,
			email,
			['sandro@sh-digital.ch','livio.bonetta@geboshop.ch'],
				)
	email.fail_silently=False
	email.content_subtype = "html"
	email.send()

	context = {

	'mp' : mp,
		
				}
	return render(request, 'marktplatz/marktplatz-erfolg.html', context)

@login_required
def marktplatz_inserat_erfassen(request):
	if request.method == "POST":
		form = InseratCreateForm(request.POST or None,request.FILES or None,)
		if form.is_valid():
			mp = form.save(commit=False)
			mp.user = request.user
			mp.save()
			
			return redirect('store:marktplatz_inserat_summary', pk=mp.id)

		else:
			messages.error(request, "Error")

	else: 
		form = form = InseratCreateForm()

	context = {
		'form': form,
				}
	return render(request, 'marktplatz/marktplatz-inserat-erfassen.html', context)

@login_required
def marktplatz_inserat_ändern(request, pk):
	inserat = get_object_or_404(Marketplace, id=pk)
	
	if request.method == "POST":
		form = InseratCreateForm(request.POST or None, request.FILES or None, instance=inserat)
		if form.is_valid():
			mp = form.save(commit=False)
			mp.user = request.user
			mp.save()
			return redirect('store:marktplatz_inserat_summary', pk=mp.id)

		else:
			messages.error(request, "Error")

	else: 
		form = form = InseratCreateForm(instance=inserat)

	context = {
		'form': form,
				}
	return render(request, 'marktplatz/marktplatz-inserat-erfassen.html', context)

def marktplatz_main(request):
	

	mp_inserate = Marketplace.objects.all()

	mp_categories = MP_Category.objects.all()

	context = {

	'mp_inserate': mp_inserate,
	'mp_categories': mp_categories,
	

	}
	return render (request, 'marktplatz/marktplatz-main.html', context)





#myinserate benutzer übersicht

@login_required
def myinserate(request):
	myinserat = Marketplace.objects.filter(user=request.user)

	context = { 
			'myinserat': myinserat,
			
			}
	return render(request, 'marktplatz/marktplatz-inserate-benutzer.html', context)


@login_required
def myinserate_löschen(request, pk):
	element = get_object_or_404(Marketplace, pk=pk)
	if request.method == "POST":
		return redirect("store:myinserate-wirklich", pk=pk)

	else:
		messages.info(request, "Achtung!")
		context = {
		'element': element,
				}
		return render(request, 'marktplatz/marktplatz-inserate-wirklich-loeschen.html', context)


@login_required
def myinserate_wirklich(request, pk):
	eintrag = get_object_or_404(Marketplace, pk=pk)
	eintrag.delete()
	messages.info(request, "Das Inserat wurde gelöscht.")
	return redirect("store:myinserate")

@login_required
def myinserate_ändern(request, pk):
	inserat = get_object_or_404(Marketplace, id=pk)
	
	if request.method == "POST":
		form = InseratCreateForm(request.POST or None, request.FILES or None, instance=inserat)
		if form.is_valid():
			mp = form.save(commit=False)
			mp.user = request.user
			mp.save()
			return redirect('store:myinserate')

		else:
			messages.error(request, "Error")

	else: 
		form = form = InseratCreateForm(instance=inserat)

	context = {
		'form': form,
				}
	return render(request, 'marktplatz/marktplatz-inserate-benutzer-edit.html', context)

#myinserate benutzer übersicht end

def marktplatz_jobinserat_details(request, pk, slug):
	inserat = get_object_or_404(JobsMarketplace, id=pk, slug=slug)

	context = {

			'inserat' : inserat,

			}

	return render (request, 'marktplatz/marktplatz-jobinserat-details.html', context)

def marktplatz_inserat_details(request, slug):
	inserat = get_object_or_404(Marketplace, slug=slug)

	if request.user.is_authenticated:
		user = request.user 
		kunde = Kunde.objects.get(user=user)

		inserat_kunde = Kunde.objects.get(user=inserat.user)

		if request.method =="POST":
			nachricht = request.POST['message']
			

			subject = 'Anfrage für Inserat Nr. ' + str(inserat.id)
			template = render_to_string('marktplatz/inserat-verk-email.html', {
				'benutzer': user.username,
				'firma': kunde.firmenname,
				'nachricht': nachricht,	
				'inserat' : inserat,
				'email' : kunde.user.email,
				'telefon' : kunde.phone,		
				 })

			email = ''
			
			#send email for order
			email = EmailMessage(
				subject,
				template,
				email,
				[inserat.user.email],
			)

			email.fail_silently=False
			email.content_subtype = "html"
			email.send()
			messages.error(request, "Die Nachricht wurde erfolgreich gesendet")
			return redirect('store:marktplatz_inserat_details', slug=inserat.slug)

		else:
			context = {

			'inserat' : inserat,

			}
			return render (request, 'marktplatz/marktplatz-inserat-details.html', context)

	else:
		context = {

			'inserat' : inserat,

			}
		return render (request, 'marktplatz/marktplatz-inserat-details.html', context)


def marktplatz_condition(request, cond):

	if cond == "Gebraucht":
		mp_inserate = Marketplace.objects.filter(condition="G")

	elif cond == "Neu":
		mp_inserate = Marketplace.objects.filter(condition="N")

	else: 
		mp_inserate = Marketplace.objects.all()

	mp_categories = MP_Category.objects.all()

	context = {

	'mp_categories' : mp_categories,
	'mp_inserate': mp_inserate,

	}
	return render (request, 'marktplatz/marktplatz-main.html', context)


# Marktplatz CMS

@staff_member_required
def cms_inserat_freigeben(request, pk, portal):
	
	if portal == "Jobs":
		mp = get_object_or_404(JobsMarketplace, pk=pk)
		mp.is_active = True 
		mp.save()
		'''messages.info(request, "Das Inserat wurde freigegeben.")
		subject = 'Inserat Nr.' + ' ' + str(mp.id) + ' ' + mp.title + ' wurde freigegeben.'
		if mp.condition == "G":
			condition = "Gebraucht"
		else:
			condition = "Neu"
		template = render_to_string('marktplatz/inserat-email.html', {
			'title' : mp.title,
			'price': mp.price, 
			'condition': condition,
			'place': mp.place,
			'add_date': mp.add_date,
			'category': mp.category,		
					 })
		email = ''	
		#send email for order
		email = EmailMessage(
			subject,
			template,
			email,
			[mp.user.email],
				)

		email.fail_silently=False
		email.content_subtype = "html"
		email.send()'''
		return redirect("store:cms_marktplatz")
	else:
		mp = get_object_or_404(Marketplace, pk=pk)
		mp.is_active = True 
		mp.save()
		messages.info(request, "Das Inserat wurde freigegeben.")
		subject = 'Inserat Nr.' + ' ' + str(mp.id) + ' ' + mp.title + ' wurde freigegeben.'
		if mp.condition == "G":
			condition = "Gebraucht"
		else:
			condition = "Neu"
		template = render_to_string('marktplatz/inserat-email.html', {
			'title' : mp.title,
			'price': mp.price, 
			'condition': condition,
			'place': mp.place,
			'add_date': mp.add_date,
			'category': mp.category,		
					 })
		email = ''	
		#send email for order
		email = EmailMessage(
			subject,
			template,
			email,
			[mp.user.email],
				)

		email.fail_silently=False
		email.content_subtype = "html"
		email.send()
		return redirect("store:cms_marktplatz")

@staff_member_required
def cms_inserat_deaktivieren(request, pk, portal):

	if portal == "Jobs":
		mp = get_object_or_404(JobsMarketplace, pk=pk)
	else:
		mp = get_object_or_404(Marketplace, pk=pk)
	mp.is_active = False 
	mp.save()
	messages.info(request, "Das Inserat wurde deaktiviert.")
	return redirect("store:cms_marktplatz")

@staff_member_required
def cms_marktplatz(request):
	query1 = Marketplace.objects.all()
	query2 = JobsMarketplace.objects.all()
	inserate = list(chain(query1, query2))
	

	context = {
		'produkte': inserate,
	 }
	return render(request, 'marktplatz/cms-marktplatz.html', context)


@staff_member_required
def cms_mp_bearbeiten(request, pk):
	mp = get_object_or_404(Marketplace, pk=pk)
	if request.method == "POST":
		form = InseratCreateForm(request.POST or None,request.FILES or None, instance=mp)
		if form.is_valid():
			form.save()
			return redirect('store:cms_marktplatz')

		else:
			messages.error(request, "Error")
			
	else:
		form = InseratCreateForm(request.POST or None, request.FILES or None, instance=mp)
		context = {
			'form': form,
			'mp': mp,
			 }
		return render(request, 'marktplatz/cms-marktplatz-edit.html', context)

@staff_member_required
def cms_mp_löschen(request, pk):
	eintrag = get_object_or_404(Marketplace, pk=pk)
	eintrag.delete()
	messages.info(request, "Das Inserat wurde gelöscht.")
	return redirect("store:cms_marktplatz")

# Marktplatz CMS END

def marktplatz_main_category(request, cat):

	mp_inserate = Marketplace.objects.filter(category__name=cat)

	mp_categories = MP_Category.objects.all()

	context = {

	'mp_inserate': mp_inserate,
	'mp_categories': mp_categories,

	}
	return render (request, 'marktplatz/marktplatz-main.html', context)

def marktplatz_main_jobs_category(request, cat):

	mp_inserate = JobsMarketplace.objects.filter(category__name=cat)

	mp_categories = MP_JobsCategory.objects.all().order_by('name')

	context = {

	'mp_inserate': mp_inserate,
	'mp_categories': mp_categories,

	}
	return render (request, 'marktplatz/marktplatz-jobs.html', context)



def error_404(request, exception):
        data = {}
        return render(request,'404.html', data)



def searchbar(request):
	search_query = request.GET.get('search', '')
	if search_query:
		items = Item.objects.filter(Q(titel__icontains=search_query) | Q(artikelnr__icontains=search_query) | Q(kategorie__name__icontains=search_query) | Q(subkategorie__sub_name__icontains=search_query))
	else:
		items = Item.objects.all()


	context = {'items': items}
	return render(request, 'shop/searchbar.html', context)


def impressum(request):
	context = {}
	return render(request, 'impressum.html', context)


#Kontaktseite
def kontakt(request):

	if request.method =="POST":
		vorname = request.POST['message-surname']
		nachname = request.POST['message-name']
		firma = request.POST['message-company']
		email = request.POST['message-email']
		nachricht = request.POST['message']
		telefon = request.POST['message-phone']
		anrede = request.POST['message-anrede']

		subject = 'Nachricht von ' + ' '+ firma + ' ' + vorname + ' ' + nachname
		template = render_to_string('shop/kontakt-email.html', {
			'anrede' : anrede,
			'vorname': vorname, 
			'nachname': nachname,
			'firma': firma,
			'email': email,
			'telefon': telefon,
			'nachricht': nachricht,			
			 })
		
		#send email for order
		email = EmailMessage(
			subject,
			template,
			email,
			['info@gastroplatz.ch', 'sandro@sh-digital.ch'],
		)

		email.fail_silently=False
		email.content_subtype = "html"
		email.send()

		context = {
			'message_kontakt' : 'Die Nachricht wurde erfolgreich gesendet.'
			 }
		return render(request, 'kontakt.html', context)
	
	else:
		context = { }
		return render(request, 'kontakt.html', context)




@login_required
def einstellungen(request):
	address = Address.objects.get(user=request.user)
	user = request.user
	if request.method == "POST":
		firmenname = request.POST['firmenname']
		vorname = request.POST['vorname']
		nachname = request.POST['nachname']
		birthday = request.POST['birthday']
		phone = request.POST['phone']
		mobile = request.POST['mobile']
		user.profile.birthday = birthday
		user.profile.mobile = mobile
		user.profile.phone = phone
		user.profile.firmenname = firmenname
		user.profile.save()
		user.first_name = vorname
		user.last_name = nachname
		user.save()
		form = AddressForm(request.POST or None, instance=address)
		if form.is_valid():
			form.save()
			return redirect('store:einstellungen')

		else:
			messages.error(request, "Error")

	else: 
		form = AddressForm(request.POST or None, instance=address)

	context = {
		'form': form,
		'address' : address,
				}
	return render(request, 'shop/einstellungen.html', context)	



#CMS related fields --- only for staff available
@staff_member_required
def cms(request):

	context = { }
	return render(request, 'cms.html', context)




@staff_member_required
def cms_kunden(request):
	user = User.objects.all().order_by('-id')
	search_query = request.GET.get('search', '')


	if search_query:
		user = User.objects.filter(Q(profile__firmenname__icontains=search_query) | Q(profile__interne_nummer__icontains=search_query))

	else:
		user = User.objects.all().order_by('-id')
			

	context = {
			'user': user,		
			 }
	return render(request, 'cms-kunden.html', context)

@login_required
def cms_user(request):
	user = User.objects.all().order_by('-date_joined')
	context = {
			'user': user,
			 }
	return render(request, 'cms-user.html', context)

@staff_member_required
def cms_kunden_erfassen(request):
	if request.method == "POST":
		form = KundeCreateForm(request.POST or None)
		if form.is_valid():
			new_user = User.objects.create_user(**form.cleaned_data)
			new_kunde = Kunde.objects.create(user=new_user, firmenname=request.POST['username'], rabatt=0)
			new_kunde.save()
			new_address = Address.objects.create(user=new_user, rechnung_strasse='Bitte ändern')
			
			return redirect('store:cms_kunden')

		else:
			messages.error(request, "Error")

	else: 
		form = form = KundeCreateForm()

	context = {
		'form': form,
				}
	return render(request, 'cms-kunden-erfassen.html', context)


@login_required
def cms_firmenname_bearbeiten(request, user_id):
	kunde = get_object_or_404(Kunde, user_id=user_id)
	if request.method == "POST":
		form = KundeEditForm(request.POST or None, request.FILES or None, instance=kunde)
		if form.is_valid():
			form.save()
			return redirect('store:cms_kunden')

		else:
			messages.error(request, "Error")
			
	else:
		form = KundeEditForm(request.POST or None, request.FILES or None, instance=kunde)
		context = {
			'form': form,
			'kunde': kunde,
			 }
		return render(request, 'cms-kunden-firmenname-bearbeiten.html', context)

@staff_member_required
def cms_user_bearbeiten(request, pk):
	kunde = get_object_or_404(User, pk=pk)
	if request.method == "POST":
		form = KundeEditForm(request.POST or None, request.FILES or None, instance=kunde)
		if form.is_valid():
			form.save()
			return redirect('store:cms_kunden')

		else:
			messages.error(request, "Error")
			
	else:
		form = KundeEditForm(request.POST or None, instance=kunde)
		context = {
			'form': form,
			'kunde': kunde,
			 }
		return render(request, 'cms-user-bearbeiten.html', context)


@staff_member_required
def cms_kunde_bearbeiten(request, pk):
	kunde = get_object_or_404(Kunde, pk=pk)
	if request.method == "POST":
		form = KundeEditAdvancedForm(request.POST or None, instance=kunde)
		if form.is_valid():
			form.save()
			return redirect('store:cms_kunden')

		else:
			messages.error(request, "Error")
			
	else:
		form = KundeEditAdvancedForm(request.POST or None, request.FILES or None, instance=kunde)
		context = {
			'form': form,
			'kunde': kunde,
			 }
		return render(request, 'cms-kunden-bearbeiten.html', context)

@staff_member_required
def cms_kundenadresse_bearbeiten(request, pk):
	kunde = get_object_or_404(User, pk=pk)
	address = Address.objects.get(user=kunde)
	if request.method == "POST":
		form = AddressForm(request.POST or None, instance=address)
		if form.is_valid():
			form.save()
			return redirect('store:cms_kunden')

		else:
			messages.error(request, "Error")
			
	else:
		form = AddressForm(request.POST or None, instance=address)
		context = {
			'form': form,
			'kunde': kunde,
			 }
		return render(request, 'cms-kundenadresse-bearbeiten.html', context)


@staff_member_required
def cms_kunde_löschen(request, pk):
	eintrag = get_object_or_404(User, pk=pk)
	eintrag.delete()
	messages.info(request, "Der Kunde wurde gelöscht.")
	return redirect("store:cms_kunden")	

@staff_member_required
def cms_kunde_löschen(request, pk):
	eintrag = get_object_or_404(User, pk=pk)
	eintrag.delete()
	messages.info(request, "Der Kunde wurde gelöscht.")
	return redirect("store:cms_kunden")	

@staff_member_required
def cms_user_bearbeiten(request, pk):
	kunde = get_object_or_404(User, pk=pk)
	if request.method == "POST":
		form = KundeEditForm(request.POST or None, request.FILES or None, instance=kunde)
		if form.is_valid():
			form.save()
			return redirect('store:cms_kunden')

		else:
			messages.error(request, "Error")
			
	else:
		form = KundeEditForm(request.POST or None, instance=kunde)
		context = {
			'form': form,
			'kunde': kunde,
			 }
		return render(request, 'cms-user-bearbeiten.html', context)


@staff_member_required
def cms_benutzerdaten(request):
	context = { }
	return render(request, 'cms-benutzerdaten.html', context)


@login_required
def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ('Erfolgreich angemeldet.'))
			return redirect ('store:cms')
		else:
			messages.success(request, ('Fehler - bitte überprüfen Sie Ihre Angaben.'))
			return redirect ('store:login_user')
	else:
		context = {}
		return render(request, 'cms-login.html', context )

@login_required
def logout_user(request):
	logout(request)
	messages.success(request, ('Sie wurden erfolgreich abgemeldet.'))
	return redirect('store:login_user')