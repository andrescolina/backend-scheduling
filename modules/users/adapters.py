from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_username, user_email, user_field

class UserAdapter(DefaultAccountAdapter):
    
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        username = data.get('username').lower()
        user_email(user, email)
        user_username(user, username)
        if first_name:
           user_field(user, 'first_name', first_name)
        if last_name:
           user_field(user, 'last_name', last_name)
        if 'password1' in data:
           user.set_password(data["password1"])
        else:
           user.set_unusable_password()
        self.populate_username(request, user)
        user.id_group_id = data.get("id_group")
        user.document = data.get("document")
        user.type_document = data.get('type_document')
        user.phone_home = data.get('phone_home')
        user.phone_mobile = data.get('phone_mobile')
        user.city = data.get('city')
        user.phone_office = data.get('phone_office')
        if commit:
                user.save()
        return user