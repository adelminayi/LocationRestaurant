from django import forms


class RestaurantModelForm(forms.Form):
    location = forms.CharField(max_length=150, label="موقعیت شما")
