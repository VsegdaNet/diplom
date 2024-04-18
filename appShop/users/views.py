from django.shortcuts import redirect, render
from orders.models import Order, OrderItem
from carts.models import Cart
from users.forms import UserLoginForm, UserRegistrationForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                return HttpResponseRedirect(reverse('main:index'))

    else:
        form = UserLoginForm()

    context = {
        'title': 'Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)

def registration(request):

    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
                form.save()

                session_key = request.session.session_key   

                user = form.instance
                auth.login(request, user)
                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Регистрация',
        'form':form
    }
    return render(request, 'users/registration.html', context)



@login_required
def profile(request):

    orders = (
        Order.objects.filter(user=request.user).prefetch_related(Prefetch("orderitem_set",
                                                                queryset=OrderItem.objects.select_related('product'),
                                                                )).order_by('-id')
            )

    context = {
        'title': 'Профиль',
        'orders': orders
    }
    return render(request, 'users/profile.html', context)




def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))


def users_card(request):
    return render(request, 'users/users_card.html')