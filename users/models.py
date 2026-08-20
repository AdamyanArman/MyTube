from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import bcrypt


# Create your models here.
class Account(models.Model):
    phone=PhoneNumberField(unique=True)
    password_hash=models.CharField(max_length=256)

    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)

    last_login=models.DateTimeField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    USERNAME_FIELD='phone'
    REQUIRED_FIELDS=[]

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.phone}'

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return True

    def set_password(self, raw_password):
        password_bytes=raw_password.encode('utf-8')
        print(f'password bytes {password_bytes}')

        salt=bcrypt.gensalt()

        hashed_password=bcrypt.hashpw(password_bytes, salt)

        print(f'hashed_password without decode {hashed_password}')
        print(f'hashed_password {hashed_password.decode("utf-8")}')
        
        self.password_hash=hashed_password.decode('utf-8')


    def check_password(self, raw_password):
        password_bytes=raw_password.encode('utf-8')

        stored_hash=self.password_hash.encode('utf-8')

        return bcrypt.checkpw(password_bytes, stored_hash)


    def save(self, *args, **kwargs):
        if not self.password_hash.startswith('$2b$'):
            self.set_password(self.password_hash)

        super().save(*args, **kwargs)

