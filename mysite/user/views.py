from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render, redirect
import re
from .models import User
from django.urls import reverse
from itsdangerous.serializer import Serializer
from django.conf import settings
from itsdangerous import SignatureExpired
from django.http.response import HttpResponse
from django.contrib.auth import login,logout, authenticate
from .models import Address
from django_redis import get_redis_connection
from goods.models import *
# Create your views here.
register_html = 'register.html'

class RegisterView(View):
    def get(self, request):
        return render(request, register_html)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')#是否同意协议

        if not all([username,password,email]):
            return render(request, register_html, {'errmsg': '数据不完整'})
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, register_html, {
                'errmsg': '邮箱格式不对'
            })
        if allow != 'on':
            return render(request, register_html, {
                'errmsg': '请同意协议'
            })
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            return render(request, register_html, {
                'errmsg': '用户名已经存在'
            })
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
        return redirect(reverse('polls:index'))


class ActiveView(View):
    def get(self, request, token):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse('激活链接已经超时')

class LoginView(View):
    def get(self, request):
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        return render(request, 'login.html', {
            'username': username,
            'checked': checked
        })
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        if not all([username, password]):
            return render(request, 'login.html', {
                'errmsg': '数据不完整'
            })
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_url = request.GET.get('next', reverse('goods:index'))
                response = redirect(next_url)
                # 判断是否需要记录用户名
                remember = request.POST.get('remember')
                if remember == 'on':
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')
                return response
            else:
                # 用户没有激活
                return render(request, 'login.html', {
                    'errmsg': '用户还没有激活'
                })
        else:
            return render(request, 'login.html', {
                'errmsg': '用户名或者密码错误'
            })
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('goods:index'))
# /user
class UserInfoView(View):
    def get(self, request):
        user = request.user
        address = Address.objects.get_default_address(user)
        con = get_redis_connection("default")
        
        history_key = 'history_{}'.format(user.id)
        # 获取用户最近浏览的5个商品
        sku_ids = con.lrange(history_key, 0, 4)
        goods_li = []
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)

        context = {
            'page': 'user',
            'address': address,
            'goods_li': goods_li
        }
        return render(request, 'user_center_info.html', context)



