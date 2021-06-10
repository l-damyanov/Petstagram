from django.urls import path

from petstagram.pets.views import list_pets, pet_details, like_pet

urlpatterns = [
    path('', list_pets, name='list pets'),
    path('detail/<int:pk>', pet_details, name='pet details'),
    path('like/<int:pk>', like_pet, name='like pet')
]
