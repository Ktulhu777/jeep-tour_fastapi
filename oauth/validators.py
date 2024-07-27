from password_validator import PasswordValidator


class ValidatePassword:
    password_validate = PasswordValidator()
    password_validate.min(8).has().digits().has().letters()

    def __call__(self, password):
        return not self.password_validate.validate(password)


password_validate = ValidatePassword()
