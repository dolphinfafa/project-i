from django.core.exceptions import MultipleObjectsReturned
from django.http import JsonResponse
from django.utils.translation import get_language
from django.views.generic import View
from django.conf import settings
import pyffx
from .forms import MessageForm
from .models import Message

ffx = pyffx.Integer(settings.PYFFX_KEY.encode(), length=5)


class MessageView(View):

    @staticmethod
    def post(request):
        form = MessageForm(request.POST)
        status_code = 201
        data = {'msg': 'ok'}
        if form.is_valid():
            message_form = form.clean()
            message_form['lang'] = get_language()
            try:
                message, created = Message.objects.get_or_create(**message_form)
            except MultipleObjectsReturned:
                pass
            # 生成消息序列号
            if created:
                if message.id and message.number is None:
                    message.number = ffx.encrypt(message.id)
                    message.save()
        else:
            data['msg'] = 'fail'
            data['errors'] = form.errors
            status_code = 400
        return JsonResponse(data=data, status=status_code)
