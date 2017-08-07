import xadmin
from .models import EmailVerifyRecord


class EmailVerifyRecordAdmin(object):
    pass

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)