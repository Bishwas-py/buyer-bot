from django import forms
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Items(models.Model):
    link = models.URLField(max_length=1299, null=True, blank=False)
    quantity = models.IntegerField(default=1, null=True, blank=False)
    min_price = models.FloatField(default=0, null=True, blank=False,
        verbose_name="Minimum Price")
    max_price = models.FloatField(null=True, blank=False, 
        verbose_name="Maximum Price", help_text="Remember MAX price must be greater than MIN.")
    security_code = models.CharField(null=True, blank=False, max_length=500)
    account = models.OneToOneField('Accounts', on_delete=models.SET_NULL, null=True)
    profile_suffix = models.CharField(default="NEW_ITEM", null=True, blank=False, max_length=500,
        help_text='Profile suffix is used for cache storing (Saving account).')
    skip = models.BooleanField(default=False, null=True, blank=False,
        help_text='Enable `Skip` if you think login process is not required to do again and again.')
    bought = models.BooleanField(default=False)
    is_test = models.BooleanField(default=False, help_text="Enable test only for testing purpose.")
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def clean(self):
        if "bestbuy.com" not in self.link:
            raise ValidationError("Well! The link you're trying to save doesn't belog to bestbuy.com")
        if self.min_price >= self.max_price:
            raise ValidationError("Minimum price is greater than maximum price.")

    def __str__(self) -> str:
        return self.link
    
    def save(self, *args, **kwargs):
        from .machine.main import threads
        if threads:
            threads[self.id]['item'] = self
        super(Items, self).save(*args, **kwargs)

class Settings(models.Model):
    headless = models.BooleanField(default=False)
    refresh_delay = models.IntegerField(default=600)
    zip_code = models.CharField(null=True, blank=False, max_length=7)
    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"
    

class Tasks(models.Model):
    total_plays = models.IntegerField(default=0)

    def __str__(self):
        return "Total plays: "+ str(self.total_plays)
    
class Playlists(models.Model):
    link = models.URLField()

    def __str__(self):
        return str(self.link)
    

class Accounts(models.Model):
    email = models.CharField(null=False, blank=False, max_length=255)
    password = models.CharField(null=False, blank=False, max_length=255)
    g_password = models.CharField(null=True, blank=False, max_length=255)
    
    def __str__(self):
        return str(self.email)
    
    class Meta:
        verbose_name = "Account"
    
    
