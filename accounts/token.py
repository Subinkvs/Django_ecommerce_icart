from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import int_to_base36

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.is_active) + str(user.pk) + str(timestamp)
        )

token_generator = AccountActivationTokenGenerator()
