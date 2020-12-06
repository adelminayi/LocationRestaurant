from django.contrib.gis.db import models


# Create your models here.

class RestaurantModel(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام")
    address = models.CharField(null=True, blank=True, max_length=50, verbose_name="آدرس")
    city = models.CharField(null=True, blank=True, max_length=50, verbose_name="شهر")
    location = models.PointField(verbose_name="موقعیت جغرافیایی")
    service = models.IntegerField(verbose_name="محدوده سرویس دهی")

    @property
    def longitude(self):
        return self.location.x

    @property
    def latitude(self):
        return self.location.y

    def __str__(self):
        return f"{self.id}-restaurant : {self.name}"

    class Meta:
        verbose_name_plural = "رستوران ها"

    def get_absolute_url(self):
        return f'{self.id}/{self.name.replace(" ", "-")}'
