from django.contrib import admin

from .models import (
    Client,
    EmailBlockSending,
    Fingerprint,
    PassportData,
    PinCode,
    UserProfile,
    Verification,
)

admin.site.register(Client)
admin.site.register(PassportData)
admin.site.register(Fingerprint)
admin.site.register(UserProfile)
admin.site.register(EmailBlockSending)
admin.site.register(Verification)
admin.site.register(PinCode)
