from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import json
from django.http import JsonResponse
from django.core import serializers
from .forms import ImageUploadForm

def login(request):
    body = json.loads(request.body)
    errors = []
    if request.method == "POST":
        email = body['email']
        password = body['password']
        potential_user = User.objects.login(email, password)
        if "errors" in potential_user:
            for error in potential_user["errors"]:
                errors.append(error)
            return JsonResponse({'errors':errors})
        else:
            request.session["id"] = potential_user["user"].id
            request.session["first_name"] = potential_user["user"].first_name
            return JsonResponse({"id":potential_user["user"].id, "first_name":potential_user["user"].first_name, "picture":potential_user["user"].profile_picture})
    else:
        return JsonResponse({'error':'Wrong HTTP method'})


def create(request):
    body = json.loads(request.body)
    errors = []
    if request.method == "POST":
        first_name = body['first_name']
        last_name = body['last_name']
        email = body['email']
        username=body['username']
        if 'tag_line' in body:
            tag_line=body['tag_line']
        else:
            tag_line=""
        password = body['password']
        confirm_password = body['confirm_password']
        potential_user = User.objects.add_user(first_name, last_name, email, username, password, confirm_password, tag_line)
        if "errors" in potential_user:
            for error in potential_user["errors"]:
                errors.append(error)
            return JsonResponse({'errors':errors})
        else:
            request.session["id"] = potential_user["newuser"].id
            request.session["first_name"] = potential_user["newuser"].first_name
            # user = serializers.serialize('json', [potential_user["newuser"],], fields=('first_name'))
            # struct = json.loads(user)
            # user = json.dumps(struct[0])
            return JsonResponse({"id":potential_user["newuser"].id, "first_name": potential_user["newuser"].first_name, "picture":potential_user["newuser"].profile_picture})
    else:
        return JsonResponse({'error':'Wrong HTTP method'})

def set_picture(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user = User.objects.get(id=request.session["id"])
        user.profile_picture = body["picture"]
        user.save()
        return JsonResponse({'picture':user.profile_picture})
    return JsonResponse({'error':'Wrong HTTP method'})

def add_picture(request, id):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(id=request.session["id"])
            user.profile_picture = form.cleaned_data['image']
            user.save()
            relative_path = user.primary_image.name[17:]
            User.objects.filter(id=request.session["id"]).update(profile_picture=relative_path)
            return JsonResponse({'success':relative_path})
    return JsonResponse({'error':'Wrong HTTP method'})

def logout(request):
    del request.session['id']
    del request.session['first_name']
    return JsonResponse({"success":"Session Cleared"})

def session(request):
    if request.method == "GET":
        if 'id' in request.session:
            return JsonResponse({'id':request.session['id'], 'first_name':request.session['first_name']})
        else:
            return JsonResponse({})
    else:
        return JsonResponse({'error':'Wrong HTTP method'})
