from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import (
	Group, Permission, PermissionsMixin, AbstractBaseUser, 
	UserManager, Permission, PermissionsMixin, AbstractBaseUser, UserManager, 
	_user_has_perm
)
from django.utils import timezone

# Create your models here.
class AbstractUser(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        ('username'),
        max_length=150,
        unique=True,
        help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    email = models.EmailField(
            ('email address'), 
            blank=True
        )
    first_name = models.CharField(
            max_length=150, 
            blank=False, 
            null=False, 
            default=None
        )
    last_name = models.CharField(
            max_length=150, 
            blank=True, 
            null=True, 
            default=None
        )
    is_staff = models.BooleanField(
            ('staff status'),
            default=False,
            help_text=('Designates whether the user can log into this admin site.'),
        )
    is_superuser = models.BooleanField(
            ('staff status'),
            default=False,
            help_text=('Designates whether the user can log into this admin site.'),
        )
    is_active = models.BooleanField(
        ('active'),
        default=False,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    phone_mobile = models.CharField(
            max_length=15,
            blank=True,
            null=True,
            unique=True,
            default=None,
            error_messages=
            {
                'unique': 'ya se encuentra un usuario con ese telefono'
            }
        )
    date_joined = models.DateTimeField(('date joined'), default=timezone.now)
    phone_home = models.CharField(
            max_length=15,
            blank=True,
            null=True,
            unique=True,
            default=None,
            error_messages=
            {
                'unique': 'ya se encuentra un usuario con ese telefono'
            }
        )
    phone_office = models.CharField(
            max_length=15,
            blank=True,
            null=True,
            unique=True,
            default=None,
            error_messages=
            {
                'unique': 'ya se encuentra un usuario con ese telefono'
            }
        )
    id_group = models.ForeignKey(
            Group, 
            on_delete=models.CASCADE
        )
    city = models.CharField(
            max_length=200,
            blank=True,
            null=True
        )
    type_document = models.CharField(
            max_length=2,
            blank=False,
            null=False,
            choices=[
                    ('CC', 'Cedula de ciudadania'),
                    ('TA', 'Tarjeta de identidad'),
                ]
        )
    document = models.IntegerField(
            blank=False,
            null=False
        )
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

class User(AbstractUser):

	class Meta(AbstractUser.Meta):
		swappable = 'AUTH_USER_MODEL'


class ModulesApplication(models.Model):

    name = models.CharField(
            max_length=200,
            blank=False,
            null=False
        )
    icon = models.CharField(
            max_length=200,
            blank=False,
            null=False
        )
    path = models.CharField(
            max_length=200,
            blank=False,
            null=False
        )
    nickname = models.CharField(
            max_length=200,
            blank=False,
            null=False
        )
    
    class Meta:
        db_table = "modules_aplication"

class GroupsModuls(models.Model):

    id_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    id_module = models.ForeignKey(ModulesApplication, on_delete=models.CASCADE)

    class Meta:
        db_table = "groups_modules"
