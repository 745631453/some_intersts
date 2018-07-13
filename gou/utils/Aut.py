import time
from datetime import datetime
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from Ind.models import MineModel

# 表示登录了就传入参数，同时验证是否时间过期，如果过期就删除数据库中的值，如果没有参数登录就不做处理
class Authware(MiddlewareMixin):

    def process_request(self, request):
        # 获取浏览器ticket值
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return None
        cc = MineModel.objects.filter(m_ticket=ticket)
        if cc:
            # 判断是否有效，无效就删除
            # 因为数据库自动加了8个小时所以用utcnow
            # 由于返回的参数带有replace所以需要去除它才能做比较
            if cc[0].m_time.replace(tzinfo=None) > datetime.utcnow():
                # 没有失效 就给request赋值
                request.user = cc[0].m
            else:
                cc.delete()
        return None
