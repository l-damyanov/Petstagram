from django.contrib.auth.decorators import login_required
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

    is_owner = pet.user == req.user

    is_liked_by_user = pet.like_set.filter(user_id=req.user.id).exists()

    context = {
        'pet': pet,
        'comment_form': CommentForm(
            initial={
                'pet_id': pk,
            }
        ),
        'comments': pet.comment_set.all(),
        'is_owner': is_owner,
        'is_liked': is_liked_by_user,
    }

    return render(req, 'pets/pet_detail.html', context)


def like_pet(req, pk):
    pet = Pet.objects.get(pk=pk)
    like_object_by_user = pet.like_set.filter(user_id=req.user.id).first()
    if like_object_by_user:
        like_object_by_user.delete()
    else:
        like = Like(
            pet=pet,
            user=req.user,
        )
        like.save()
    return redirect('pet details', pet.id)


@login_required
def create_pet(req):
    if req.method == 'POST':
        form = PetForm(req.POST, req.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.user = req.user
            pet.save()
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
        comment = form.save(commit=False)
        comment.user = req.user
        comment.save()

    return redirect('pet details', pk)
