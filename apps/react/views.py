from django.shortcuts import render, HttpResponse
from .models import *
from datetime import *
import json
from django.http import JsonResponse
from django.core import serializers
import datetime
from django.db.models import Q

def index(request):
    return render(request, 'react/index.html')

def home(request):
    if request.method == 'GET':
        daily_tasks = Task.objects.filter(user__id = request.session['id'], start_date = datetime.date.today())
        upcoming_tasks = Task.objects.filter(user__id = request.session['id'], start_date = datetime.date.today())
        return JsonResponse({'daily_tasks': tasks, 'upcoming_tasks': upcoming_tasks})
    else:
        return JsonResponse({'error': 'Wrong HTTP method'})

def task(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        name = body['name']
        if 'description' in body:
            description = body['description']
        else:
            description = ""
        start_date = body['start_date']
        end_date = body['end_date']
        points = body['points']
        task_type = body['task_type']
        public = body['public']
        task = Task.objects.create_task(request.session['id'], name, description, start_date, end_date, points, task_type, public)
        print task
        if 'errors' in task:
            errors = []
            for error in task["errors"]:
                errors.append(error)
            return JsonResponse({'errors':errors})
        else:
            return JsonResponse({"name":task['task'].name})
    elif request.method == 'GET':
        tasks = Task.objects.filter(user__id=request.session['id']).values('id', 'name', 'description', 'end_date', 'points', 'start_date', 'task_type', 'created_at', 'public', 'completed', 'updated_at')
        return JsonResponse({"tasks": list(tasks)})
    elif request.method == "PATCH":
        body = json.loads(request.body)
        task_id = body['id']
        name = body['name']
        description = body['description']
        start_date = body['start_date']
        end_date = body['end_date']
        points = body['points']
        task_type = body['task_type']
        public = body['public']
        updated_task = Task.objects.update_task(task_id, name, description, start_date, end_date, points, task_type, public)
        if body['completed'] == True:
            updated_task = Task.objects.completed_task(request.session['id'], task_id)
        print updated_task
        if 'errors' in updated_task:
            errors = []
            for error in updated_task["errors"]:
                errors.append(error)
            return JsonResponse({'errors':errors})
        else:
            return JsonResponse({'Success':True})
    return JsonResponse({'error':'Wrong HTTP method'})

def group(request):
    body = json.loads(request.body)
    if request.method == 'POST':
        name = body['name']
        wager_amount = body['wager_amount']
        task_id = body['task_id']
        new_group = Group.objects.create_group(name, wager_amount, task_id)
        if new_group:
            new_member = GroupMember.objects.create_member(new_group.group.id, request.session['id'])
    elif request.method == 'GET':
        groups = Group.objects.filter(task__user__id = request.session['id'])
        return JsonResponse({'group':groups})

def add_member(request):
    body = json.loads(request.body)
    if request.method == 'POST':
        group_id = body['group_id']
        new_member = GroupMember.objects.create_member(group_id, request.session['id'])
    if request.method == 'PUT':
        if body['status'] == 'accept':
            group_id = body['group_id']
            group = GroupMember.objects.accepted(group_id, request.session['id'])
        else:
            group_member_id = body['group_member']
            group = GroupMember.objects.denied(group_member_id)
        return JsonResponse({'Success': 'Group member changed'})
    else:
        return JsonResponse({'error':'Wrong HTTP method'})

def activity_feed(request):
    if request.method == 'GET':
        pass
    else:
        return JsonResponse({'error': 'Wrong HTTP method'})

def points(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.session['id'])
        return JsonResponse({'open_balance':user.open_balance, 'wager_balance':user.wager_balance, 'spent':user.spent})
    else:
        return JsonResponse({'error':'Wrong HTTP method'})

def user_search(request):
    if request.method == 'GET':
        term = request.GET['props']
        friends = Friend.objects.filter(user=request.session['id']).values_list('friend', flat=True)
        users = User.objects.filter(username__contains=term).exclude(id__in=friends).exclude(id=request.session['id']).values('first_name', 'last_name', 'tag_line', 'username', 'profile_picture', 'id')
        if 'errors' in users:
            errors = []
            for error in task["errors"]:
                errors.append(error)
            return JsonResponse({'errors':errors})
        else:
            return JsonResponse({"users": list(users), "term": term})
    else:
        return JsonResponse({'error': 'Wrong HTTP method'})

def request_friend(request):
    if request.method == 'GET':
        id = request.GET['props']
        friend = Friend.objects.create_friend(request.session['id'],id)
        if 'errors' in friend:
            errors = []
            for error in friend["errors"]:
                errors.append(error)
            return JsonResponse({'errors':errors})
        else:
            return JsonResponse({'Success':True})
    elif request.method == 'PUT':
        body = json.loads(request.body)
        if body['status'] == 'accept':
            friend = Friend.objects.accepted(request.session['id'], body['friend'])
        else:
            friend = Friend.objects.denied(body['friendship_id'])
        return JsonResponse({'Success':'Friend changed'})

    else:
        return JsonResponse({'error': 'Wrong HTTP method'})

def create_store_item(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        print body
        name = body['name']
        price = body['price']
        picture = body['picture']
        category = body['category']
        item = StoreImage.objects.create_item(category, name, price, picture)
        if 'errors' in item:
            errors = []
            for error in item["errors"]:
                errors.append(error)
            return JsonResponse({'errors':errors})
        else:
            return JsonResponse({'Success':True})
    else:
        return JsonResponse({'error':'Wrong HTTP method'})

def store(request):
    if request.method == 'GET':
        items = StoreImage.objects.all().exclude(images_purchased__user__id=request.session['id']).values('id', 'name', 'picture', 'price', 'category')
        return JsonResponse({"items": list(items)})
    if request.method == 'POST':
        body = json.loads(request.body)
        print body
        item_id = body['item_id']
        purchase = UserImage.objects.create_user_purchase(request.session['id'], item_id)
        if 'errors' in purchase:
            errors = []
            for error in purchase["errors"]:
                errors.append(error)
            return JsonResponse({'errors':errors})
        else:
            return JsonResponse({'Success':purchase['image']})
    else:
        return JsonResponse({'error':'Wrong HTTP method'})

def purchases(request):
        if request.method == 'GET':
            purchases = StoreImage.objects.filter(images_purchased__user__id=request.session['id']).values("id","name", "picture", "category")
            return JsonResponse({"purchases": list(purchases)})
        else:
            return JsonResponse({'error':'Wrong HTTP method'})

def friends(request):
        if request.method == 'GET':
            friends = User.objects.filter(friended_users__user=request.session['id'], friended_users__accepted=True).values("id","first_name", "last_name", "username", "profile_picture", "tag_line", "open_balance", "wager_balance", "updated_at")
            return JsonResponse({"friends": list(friends)})
        else:
            return JsonResponse({'error':'Wrong HTTP method'})

def friend_tasks(request, id):
        if request.method == 'GET':
            friend_tasks = Task.objects.filter(user__id=id, public=True).values('id', 'name', 'description', 'end_date', 'points', 'start_date', 'task_type', 'public')
            return JsonResponse({"friend_tasks": list(friend_tasks)})
        else:
            return JsonResponse({'error':'Wrong HTTP method'})

def graph(request, id):
    if request.method == 'GET':
        tasks = Task.objects.filter(user__id=id)
        return JsonResponse({'tasks': tasks})

def get_requests(request):
    if request.method == 'GET':
        group_requests = GroupMember.objects.filter(user__id = request.session['id'], accepted = False).values('group__task__user__username', 'group__name', 'user_id', 'id', 'group_id' )
        # wager_requests = Wager.objects.filter(task__user__id = request.session['id'], accepted = False, task__end_date__gte=datetime.date.today()).values('points', 'wagerer', 'task__name', 'id')
        friend_requests = Friend.objects.filter(friend__id = request.session['id'], accepted = False).values('user__username', 'user__first_name', 'user__last_name', 'user_id', 'id')
        return JsonResponse ({
            'friend_requests': list(friend_requests),
            'group_requests': list(group_requests),
            })
    else:
        return JsonResponse({ 'error': 'Wrong HTTP method'})


def wagers(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        task_id = body['task']
        wager_amount = int(body['wager'])
        wager = Wager.objects.create_wager(request.session['id'], task_id, wager_amount)
        if 'errors' in wager:
            errors = []
            for error in wager["errors"]:
                errors.append(error)
            return JsonResponse({'errors':errors})
        else:
            return JsonResponse({'Success':'true'})
    elif request.method == 'GET':
        wagers = Wager.objects.filter(Q(wagerer=request.session['id']) | Q(task__user=request.session['id'])).values("id", "points", "accepted", "wagerer", "wagerer__username", "task", "task__name", "task__end_date", "task__user")
        wagers = list(wagers)
        for wager in wagers:
            wager['current_user'] = request.session['id']
        return JsonResponse({"wagers": wagers})
    elif request.method == 'PUT':
        body = json.loads(request.body)
        if body['status'] == 'accept':
            wager = Wager.objects.accepted(request.session['id'], body['wager'])
        else:
            wager = Wager.objects.denied(body['wager'])
        return JsonResponse({'Success':'Wager changed'})
    else:
        return JsonResponse({'error': 'Wrong HTTP method'})
