from django.db import models
from django.dispatch import receiver
from django.core.exceptions import ValidationError


# Create your models here.
class Items(models.Model):
    link = models.URLField(max_length=1299, null=True, blank=False)
    quantity = models.IntegerField(default=1, null=True, blank=False)
    skip = models.BooleanField(default=False, null=True, blank=False)
    min_price = models.FloatField(default=0, null=True, blank=False,
        verbose_name="Minimum Price")
    max_price = models.FloatField(null=True, blank=False, 
        verbose_name="Maximum Price", help_text="Remember MAX price must be greater than MIN.")
        
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


class Settings(models.Model):
    headless = models.BooleanField(default=True)
    maximized = models.BooleanField(default=True)
    refresh_delay = models.IntegerField(default=600)

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
    
