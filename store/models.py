from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_extensions.db.fields import AutoSlugField
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.utils.text import slugify

ADDRESS_CHOICES = (
    ('B', 'Rechnungsadresse'),
    ('S', 'Lieferadresse'),
)

PAYMENT_CHOICES = (
	('R', 'Rechnung*'),
	('V', 'Vorkasse (2% Skonto)'),
	)

CONDITION_CHOICES = (
	('G', 'Gebraucht'),
	('N', 'Neu')
	)

ANONYM_CHOICES = (
	('Ja', 'Ja'),
	('Nein', 'Nein')
	)

JOBS_CHOICES = (
(' Aargau',' Aargau'),
(' Appenzell Innerrhoden',' Appenzell Innerrhoden'),
(' Appenzell Ausserrhoden',' Appenzell Ausserrhoden'),
(' Bern',' Bern'),
(' Basel-Landschaft',' Basel-Landschaft'),
(' Basel-Stadt',' Basel-Stadt'),
(' Freiburg',' Freiburg'),
(' Genf',' Genf'),
(' Glarus',' Glarus'),
(' Graubünden',' Graubünden'),
(' Jura',' Jura'),
(' Luzern',' Luzern'),
(' Neuenburg',' Neuenburg'),
(' Nidwalden',' Nidwalden'),
(' Obwalden',' Obwalden'),
(' St. Gallen',' St. Gallen'),
(' Schaffhausen',' Schaffhausen'),
(' Solothurn',' Solothurn'),
(' Schwyz',' Schwyz'),
(' Thurgau',' Thurgau'),
(' Tessin',' Tessin'),
(' Uri',' Uri'),
(' Waadt',' Waadt'),
(' Wallis',' Wallis'),
(' Zug',' Zug'),
(' Zürich',' Zürich')
)






class MP_JobsCategory(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255)

	class Meta:
		ordering = ['id']
		verbose_name = 'MP_JobsKategorie'
		verbose_name_plural = 'MP_JobsKategorien'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('home')


class JobsMarketplace(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255)
	jobdescription = models.CharField(max_length=1000, default='')
	add_date = models.DateTimeField(auto_now_add=True)
	category = models.ForeignKey(MP_JobsCategory, related_name='mp_jobscategory', default=None, on_delete=models.SET_NULL, null=True, blank=True)
	is_active = models.BooleanField(default=False)
	payment = models.BooleanField(default=False)
	tid = models.IntegerField(null=True, blank=True)
	requirements = models.CharField(max_length=1000, default='')
	language = models.CharField(max_length=255, default='')
	res_description = models.CharField(max_length=255, default='')
	contact_person = models.CharField(max_length=255, default='')
	place = models.CharField(max_length=255, default='')
	region = models.CharField(max_length=255, choices=JOBS_CHOICES, default="Zürich")
	datejob = models.CharField(max_length=255, default='')
	kindof = models.CharField(max_length=255, default='')
	pensum = models.CharField(max_length=255, default='')
	check_portal = models.CharField(max_length=255, default='Jobs')

	class Meta:
		ordering = ['-add_date']
		verbose_name = 'JobMarketplace'
		verbose_name_plural = 'JobMarketplaces'

	def mp_firmenname(self):
		if self.user.profile.firmenname:
			mp_firmenname = self.user.profile.firmenname
			return mp_firmenname 
		else:
			mp_firmenname = self.user.username 
			return mp_firmenname

	def mp_phone(self):
		if self.user.profile.phone:
			mp_phone = self.user.profile.phone
			return mp_phone 
		else:
			mp_phone = " "
			return mp_phone

	def mp_mobile(self):
		if self.user.profile.phone:
			mp_mobile = self.user.profile.mobile
			return mp_mobile 
		else:
			mp_mobile = " "
			return mp_mobile

	def mp_email(self):
		if self.user.email:
			mp_email = self.user.email
			return mp_email 
		else:
			mp_email = " "
			return mp_email

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(JobsMarketplace, self).save(*args, **kwargs)

	def __str__(self):
		return self.title

class MP_Category(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255)

	class Meta:
		ordering = ['id']
		verbose_name = 'MP_Kategorie'
		verbose_name_plural = 'MP_Kategorien'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('home')

		
class Marketplace(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255)
	price = models.FloatField(null=True, blank=True,)
	description = models.CharField(max_length=255, default='')
	condition = models.CharField(max_length=255, choices=CONDITION_CHOICES, default="G")
	place = models.CharField(max_length=255, null=True, blank=True)
	image = models.ImageField(null=True, blank=True, upload_to="bilder/")
	image1 = models.ImageField(null=True, blank=True, upload_to="bilder/")
	image2 = models.ImageField(null=True, blank=True, upload_to="bilder/")
	add_date = models.DateTimeField(auto_now_add=True)
	category = models.ForeignKey(MP_Category, related_name='mp_category', default=None, on_delete=models.SET_NULL, null=True, blank=True)
	is_active = models.BooleanField(default=False)
	payment = models.BooleanField(default=False)
	tid = models.IntegerField(null=True, blank=True)
	numberof = models.IntegerField(null=True, blank=True)
	marke_ins = models.CharField(max_length=255,null=True, blank=True)
	typ_marke_ins = models.CharField(max_length=255,null=True, blank=True)
	anonym_ins = models.CharField(max_length=255, choices=ANONYM_CHOICES, default="Ja")


	class Meta:
		ordering = ['-add_date']
		verbose_name = 'Marketplace'
		verbose_name_plural = 'Marketplaces'

	def mp_firmenname(self):
		if self.user.profile.firmenname:
			mp_firmenname = self.user.profile.firmenname
			return mp_firmenname 
		else:
			mp_firmenname = self.user.username 
			return mp_firmenname

	def mp_phone(self):
		if self.user.profile.phone:
			mp_phone = self.user.profile.phone
			return mp_phone 
		else:
			mp_phone = " "
			return mp_phone

	def mp_mobile(self):
		if self.user.profile.phone:
			mp_mobile = self.user.profile.mobile
			return mp_mobile 
		else:
			mp_mobile = " "
			return mp_mobile

	def mp_email(self):
		if self.user.email:
			mp_email = self.user.email
			return mp_email 
		else:
			mp_email = " "
			return mp_email

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Marketplace, self).save(*args, **kwargs)

	def __str__(self):
		return self.title


class Subcategory(models.Model):
	sub_name = models.CharField(max_length=255)
	sub_slug = models.SlugField(max_length=255)

	class Meta:
		ordering = ['sub_name']
		verbose_name = 'Subkategorie'
		verbose_name_plural = 'Subkategorien'

	def __str__(self):
		return self.sub_name


class Category(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255)
	categorypic = models.ImageField(null=True, blank=True, upload_to="produktbilder/")

	class Meta:
		ordering = ['id']
		verbose_name = 'Kategorie'
		verbose_name_plural = 'Kategorien'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('home')



class Address(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name ='address', on_delete=models.CASCADE)
	rechnung_strasse = models.CharField(max_length=255)
	rechnung_nr = models.CharField(max_length=255)
	rechnung_ort = models.CharField(max_length=255)
	rechnung_land = CountryField(multiple=False)
	rechnung_plz = models.CharField(max_length=255)
	address_type = models.CharField(max_length=500, choices=ADDRESS_CHOICES)

	class Meta:
		verbose_name = 'Rechnungsadresse'
		verbose_name_plural = 'Rechnungsadressen'

	def __str__(self):
		return self.user.username + ' ' + str(self.rechnung_strasse) + ' '+ str(self.rechnung_nr) + ', ' + str(self.rechnung_plz) + ' '+ str(self.rechnung_ort)


class ShippingAddress(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name ='shipping_address', on_delete=models.CASCADE)
	lieferung_strasse = models.CharField(max_length=255)
	lieferung_nr = models.CharField(max_length=255)
	lieferung_ort = models.CharField(max_length=255)
	lieferung_land = CountryField(multiple=False)
	lieferung_plz = models.CharField(max_length=255)
	address_type = models.CharField(max_length=500, choices=ADDRESS_CHOICES)
	vorname = models.CharField(max_length=255, null=True, blank=True)
	nachname = models.CharField(max_length=255, null=True, blank=True)
	firmenname = models.CharField(max_length=255, null=True, blank=True)

	class Meta:
		verbose_name = 'Lieferadresse'
		verbose_name_plural = 'Lieferadressen'

	def __str__(self):
		return self.user.username + ' ' + str(self.lieferung_strasse) + ' '+ str(self.lieferung_nr) + ', ' + str(self.lieferung_plz) + ' '+ str(self.lieferung_ort)


class Kunde(models.Model):
	user = models.OneToOneField(User, unique=True, related_name ='profile', on_delete=models.CASCADE)
	firmenname = models.CharField(max_length=255, null=True, blank=True)
	rabatt = models.FloatField(null=True, blank=True)
	newsletter = models.BooleanField(null=True, blank=True)
	mobile = models.CharField(max_length=255, null=True, blank=True) 
	phone = models.CharField(max_length=255, null=True, blank=True) 
	birthday = models.CharField(max_length=255, null=True, blank=True)
	interne_nummer = models.IntegerField(null=True, blank=True)

	class Meta:
		ordering = ['id']
		verbose_name = 'Kunde'
		verbose_name_plural = 'Kunden'

	def __str__(self):
		return self.firmenname

	def get_absolute_url(self):
		return reverse('store:cms_kunde_bearbeiten', kwargs={'pk': self.pk})

	def get_absolute_address_url(self):
		return reverse('store:cms_kundenadresse_bearbeiten', kwargs={'pk': self.pk})

	def get_absolute_elemente_url(self):
		return reverse('store:cms_elemente', kwargs={'pk': self.pk})

