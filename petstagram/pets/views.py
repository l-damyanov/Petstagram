from django.shortcuts import render, redirect

from petstagram.common.forms import CommentForm
from petstagram.common.models import Comment
from petstagram.pets.forms import PetForm, EditPetForm
from petstagram.pets.models import Pet, Like


def list_pets(req):
    all_pets = Pet.objects.all()

    context = {
        'pets': all_pets,
    }

    return render(req, 'pets/pet_list.html', context)


def pet_details(req, pk):
    pet = Pet.objects.get(pk=pk)
    pet.likes_count = pet.like_set.count()

    context = {
        'pet': pet,
        'comment_form': CommentForm(
            initial={
                'pet_id': pk,
            }
        ),
        'comments': pet.comment_set.all(),
    }

    return render(req, 'pets/pet_detail.html', context)


def like_pet(req, pk):
    pet_to_like = Pet.objects.get(pk=pk)
    like = Like(
        pet=pet_to_like,
    )
    like.save()
    return redirect('pet details', pet_to_like.id)


def create_pet(req):
    if req.method == 'POST':
        form = PetForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
            return redirect('list pets')
    else:
        form = PetForm()

    context = {
        'form': form,
    }

    return render(req, 'pets/pet_create.html', context)


def edit_pet(req, pk):
    pet = Pet.objects.get(pk=pk)
    if req.method == 'POST':
        form = EditPetForm(req.POST, req.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('list pets')
    else:
        form = EditPetForm(instance=pet)

    context = {
        'form': form,
        'pet': pet,
    }

    return render(req, 'pets/pet_edit.html', context)


def delete_pet(req, pk):
    pet = Pet.objects.get(pk=pk)
    if req.method == 'POST':
        pet.delete()
        return redirect('list pets')
    else:
        context = {
            'pet': pet,
        }
        return render(req, 'pets/pet_delete.html', context)


# def comment_pet(req, pk):
#     pet = Pet.objects.get(pk=pk)
#     form = CommentForm(req.POST)
#     if form.is_valid():
#         comment = Comment(
#             text=form.cleaned_data['text'],
#             pet=pet,
#         )
#         comment.save()
#
#     return redirect('pet details', pet.id)

def comment_pet(req, pk):
    form = CommentForm(req.POST)
    if form.is_valid():
        form.save()

    return redirect('pet details', pk)
