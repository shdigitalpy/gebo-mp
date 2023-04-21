from django import forms
from .models import *
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template

PAYMENT_CHOICES = (
	('R', 'Rechnung*'),
	('V', 'Vorkasse (2% Skonto)'),
	)

COUNTRY_CHOICES = [
	('S', 'Schweiz'),
	('D', 'Deutschland'),
	('A', 'Österreich'),

	]


class InseratJobsCreateForm(forms.ModelForm):
	class Meta:
		model = JobsMarketplace
		fields = ('category','title','datejob','kindof','pensum', 'jobdescription', 'requirements','language','res_description','contact_person', 'place','region'  )

		labels = {
			'title' : "Titel des Eintrags:",
			'jobdescription' : "Job Beschreibung",
			'category' : "Kategorie",
			'requirements' : "Anforderungen",
			'res_description' : "Restaurant Beschreibung",
			'contact_person' : "Kontaktperson",
			'language' : "Sprachen",
			'place' : "Adresse",
			'datejob' : "Stellenantritt",
			'kindof' : "Anstellungsart",
			'pensum' : "Pensum",
			'region' : "Region"
		}
		
		widgets = {
			
			'title': forms.TextInput(attrs={
				'class': 'form-control col-6',
				'placeholder':'z.B. Küchenchef'}),
			'jobdescription': forms.Textarea(attrs={

				'class': 'form-control col-6',
				'placeholder':'Beschreibung Aufgaben'}),
			'datejob': forms.TextInput(attrs={
				'class': 'form-control col-6',
				'placeholder':'z.B. per sofort oder nach Vereinbarung'}),
			'kindof': forms.TextInput(attrs={
				'class': 'form-control col-6',
				'placeholder':'z.B. Dauerstelle/Teilzeitstelle'}),
			'pensum': forms.TextInput(attrs={
				'class': 'form-control col-6',
				'placeholder':'z.B. 100%'}),
			'language': forms.TextInput(attrs={
				'class': 'form-control col-6',
				'placeholder':'z.B. Deutsch, Englisch erwünscht'}),
			'category' : forms.Select(attrs={
				'class': 'form-control col-6',
				}),
			'requirements': forms.Textarea(attrs={
				'class': 'form-control col-6',
				'placeholder':'z.B. Kochlehre und Erfahrung in ähnlicher führender Position'}),
			'res_description': forms.Textarea(attrs={
				'class': 'form-control col-6',
				'placeholder':'z.B. Bestens frequentierter Betrieb.'}),
			'contact_person': forms.TextInput(attrs={
				'class': 'form-control col-6',
				'placeholder':'z.B. Herr Markus Müller, Geschäftsführer'}),
			'place': forms.TextInput(attrs={
				'class': 'form-control col-6',
				'placeholder':'z.B. Landstrasse 4, 8447 Dachsen'}),
			'region' : forms.Select(attrs={
				'class': 'form-control col-6',
				}),

			
		}



class InseratCreateForm(forms.ModelForm):
	class Meta:
		model = Marketplace
		fields = ('category','numberof', 'title', 'price', 'description', 'condition', 'marke_ins', 'typ_marke_ins', 'place','image','image1','image2','anonym_ins'  )

		labels = {
			'title' : "Titel des Eintrags:",
			'numberof' : "Stückzahl",
			'price' : "Preis",
			'description' : "Beschreibung",
			'condition' : "Zustand",
			'place' : "Standort",
			'image' : "Bild",
			'image1' : "Bild",
			'image2' : "Bild",
			'category' : "Kategorie",
			'anonym_ins' : "Veröffentlichung Adresse & Angaben",
			'marke_ins' : "Marke",
			'typ_marke_ins' : "Typ Bezeichnung"


		}
		

		widgets = {
			
			'title': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':'z.B. Küchenmaschine'}),
			'marke_ins': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':'Markenname'}),
			'typ_marke_ins': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':'Typ Bezeichnung'}),
			'numberof': forms.NumberInput(attrs={
				'class': 'form-control col-3',
				'placeholder':'Stückzahl'}),

			'price': forms.NumberInput(attrs={
				'class': 'form-control',
				'placeholder':'z.B. 100'}),
			'description': forms.Textarea(attrs={
				'maxlength': '100',
				'rows': '3',
				'class': 'form-control col-3',
				'placeholder':''}),
			'condition': forms.Select(attrs={
				'class': 'form-control',
				}),
			'place': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':'Wo'}),
			'image' : forms.FileInput(attrs={
				'class': 'form-control',
				}),
			'image1' : forms.FileInput(attrs={
				'class': 'form-control',
				}),
			'image2' : forms.FileInput(attrs={
				'class': 'form-control',
				}),
			'category' : forms.Select(attrs={
				'class': 'form-control',
				}),

			'anonym_ins' : forms.Select(attrs={
				'class': 'form-control',
				}),
		}



class KundeCreateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		widgets = {
			
			'username': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':''}),
			'email': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':''}),
			'password': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':''}),
			'first_name': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':''}),
			'last_name': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':''}),
		}


class RegistrationForm(SignupForm):
	username = forms.CharField(max_length=500, required=True, label="",
					widget=forms.TextInput(attrs={
						'placeholder': 'Benutzername',
						'class': 'form-control',
						}),
					help_text='Bitte einen gültigen Benutzernamen eingeben'
					)

	first_name = forms.CharField(max_length=500, required=True, label="",
					widget=forms.TextInput(attrs={
						'placeholder': 'Vorname',
						'class': 'form-control',
						}),
					help_text='Bitte einen gültigen Vornamen eingeben')

	last_name = forms.CharField(max_length=500, required=True, label="",
					widget=forms.TextInput(attrs={
						'placeholder': 'Nachname',
						'class': 'form-control',
						}),
					help_text='Bitte einen gültigen Nachnamen eingeben')

	email = forms.EmailField(max_length=500, required=True, label="",
					widget=forms.EmailInput(attrs={
						'placeholder': 'E-Mail Adresse',
						'required': True, 
						'class': 'form-control',
						'type': 'email'
						}),
					help_text='Bitte eine gültige E-Mail Adresse eingeben')

	firmenname = forms.CharField(max_length=500, required=False, label="",
					widget=forms.TextInput(attrs={
						'placeholder': 'Firmenname',
						'class': 'form-control'

						}))

	strasse = forms.CharField(max_length=500, required=True, label="Adresse",
					widget=forms.TextInput(attrs={
						'placeholder': 'Strasse',
						'class': 'form-control'

						}),
					help_text='Bitte eine gültige Strasse eingeben')

	nr = forms.CharField(max_length=500, required=True, label="",
					widget=forms.TextInput(attrs={
						'placeholder': 'Nr.',
						'class': 'form-control'

						}),
					help_text='Bitte eine gültige Strassen-Nr. eingeben')

	plz = forms.CharField(max_length=500, required=True, label="",
					widget=forms.TextInput(attrs={
						'placeholder': 'PLZ',
						'class': 'form-control'

						}))

	ort = forms.CharField(max_length=500, required=True, label="",
					widget=forms.TextInput(attrs={
						'placeholder': 'Ort',
						'class': 'form-control'

						}),
					help_text='Bitte einen gültigen Ort eingeben')

	phone = forms.CharField(max_length=500, required=True, label="",
					widget=forms.TextInput(attrs={
						'placeholder': 'Telefon / Mobile-Nr.',
						'class': 'form-control'

						}),
					help_text='Bitte eine gültige Telefon oder Mobile-Nr. eingeben')

	mobile = forms.CharField(max_length=500, required=False, label="",
					widget=forms.TextInput(attrs={
						'placeholder': 'Mobile-Nr.',
						'class': 'form-control'

						}))

	land = CountryField().formfield(
					widget=forms.Select(attrs={
						'class': 'form-control'

						}),
					help_text='Bitte ein gültiges Land auswählen')
	newsletter = forms.BooleanField(required=False)

	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields['email'].label = ""
		self.fields['password1'].label = "Passwort:"
		self.fields['password2'].label = "Passwort (wiederholen):"
		self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Passwort'})
		self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Passwort wiederholen'})
		

	def signup(self, request, user):
		user.username = self.cleaned_data['username']
		user.email = self.cleaned_data['email']
		user.password1 = self.cleaned_data['password1']
		user.password2 = self.cleaned_data['password2']
		user.save()
		return user

	def save(self, request):
		user = super(RegistrationForm, self).save(request)
		kunde, created = Kunde.objects.get_or_create(user=user)
		kunde.firmenname = self.cleaned_data['firmenname']
		kunde.newsletter = self.cleaned_data['newsletter']
		kunde.phone = self.cleaned_data['phone']
		kunde.mobile = self.cleaned_data['mobile']
		kunde.rabatt = 0
		kunde.save()
		address, created = Address.objects.get_or_create(user=user)
		address.user.first_name = self.cleaned_data['first_name']
		address.user.last_name = self.cleaned_data['last_name']
		address.rechnung_strasse = self.cleaned_data['strasse']
		address.rechnung_nr = self.cleaned_data['nr']
		address.rechnung_ort = self.cleaned_data['ort']
		address.rechnung_land = self.cleaned_data['land']
		address.rechnung_plz = self.cleaned_data['plz']
		address.address_type = "B"
		address.save()
		#email
		firmenname = self.cleaned_data['firmenname']
		username = user.username
		phone = self.cleaned_data['phone']
		mobile = self.cleaned_data['mobile']
		plz = self.cleaned_data['plz']
		ort = self.cleaned_data['ort']
		subject = 'Registration Neuer Kunde'
		template = render_to_string('shop/registration-email.html', {
			
			'firmenname': firmenname, 
			'username': username,
			'phone': phone,
			'mobile': mobile,
			'plz': plz,
			'ort': ort,			
			 })
		
		#send email for order
		email = ''
		email = EmailMessage(
			subject,
			template,
			email,
			['bestellungen@gastrodichtung.ch', 'livio.bonetta@geboshop.ch', 'sandro@sh-digital.ch'],
		)

		email.fail_silently=False
		email.content_subtype = "html"
		email.send()
		return user



class AddressForm(forms.ModelForm):
	class Meta:
		model = Address  # Your model
		fields = (
			'rechnung_strasse',
			'rechnung_nr',
			'rechnung_plz',
			'rechnung_ort',
			'rechnung_land',
			'address_type'
			
			 )
		labels = {
			'rechnung_strasse' : "Strasse:",
			'rechnung_nr' : "Nr.",
			'rechnung_ort' : "Ort",
			'rechnung_land' : "Land",
			'rechnung_plz' : "PLZ",
			'address_type' : "Adresse-Typ:"

		}
		widgets = {
			'rechnung_strasse': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder':'Strasse'}),
			'rechnung_nr': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder':'Nr.'}),
			'rechnung_ort': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder':'Ort'}),
			'rechnung_land': forms.Select(attrs={
				'class': 'form-control',
				}),
			'rechnung_plz': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder':'PLZ'}),
			'address_type': forms.Select(attrs={
				'class': 'form-control',
				}),
		}


class KundeEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			'date_joined',
			'is_active'
			)
		widgets = {
			
			'username': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':''}),
			'first_name': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':''}),
			'last_name': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':''}),
			'email': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':''}),
			'password': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':''}),
			'date_joined': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'readonly':'readonly'}),
		}

class KundeEditAdvancedForm(forms.ModelForm):
	class Meta:
		model = Kunde
		fields = (
			'firmenname',
			'interne_nummer',
			'rabatt',
			'newsletter',
			'phone',
			'mobile',
			'birthday'

			)
		widgets = {
			
			'firmenname': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':''}),
			'interne_nummer': forms.NumberInput(attrs={
				'class': 'form-control col-3',
				'placeholder':''}),
			'rabatt': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':''}),
			'newsletter': forms.Select(attrs={
				'class': 'form-control col-3',}),
			'phone': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':''}),
			'mobile': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':''}),
			'birthday': forms.TextInput(attrs={
				'class': 'form-control col-3',
				'placeholder':''}),
		}
