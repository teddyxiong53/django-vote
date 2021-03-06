from django.shortcuts import render, redirect
from django.core.cache import cache
from django.views.generic import View
from .models import *

# Create your views here.

def redirect_index(request):
    return redirect('/goods/index')

class IndexView(View):
    def get(self, request):
        context = cache.get('index_page_data')
        if context is None:
            print('设置缓存')
            # 获取商品的种类信息
            types = GoodsType.objects.all()
            # 获取首页轮播商品信息
            goods_banners = IndexGoodsBanner.objects.all().order_by('index')
            # 获取首页促销信息
            promotion_banners = IndexPromotionBanner.objects.all().order_by('index')
            # 获取首页展示商品分类
            for type in types:
                image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
                title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')
                # 动态给type增加属性
                type.image_banners = image_banners
                type.title_banners = title_banners

            context = {
                'types': types,
                'goods_banners': goods_banners,
                'promotion_banners': promotion_banners,

            }
            cache.set('index_page_data', context, 3600)

        user = request.user
        cart_count = 0
        if user.is_authenticated:
            pass # todo
        context.update(cart_count=cart_count)
        return render(request, 'index.html', context)

