from django.contrib.auth.models import User

for i in range(0,26):
    user=User.objects.create_user(chr(i+97), password=str(chr(i+97)+str(i+1)))
    user.is_superuser=False
    user.is_staff=True
    user.save()