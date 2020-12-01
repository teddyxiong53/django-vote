from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render, redirect
import re
from .models import User
from django.urls import reverse

# Create your views here.
register_html = 'register.html'

class RegisterView(View):
    def get(self, request):
        return render(request, register_html)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
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


