class InputError(Exception):
    def __init__(self, message):
        self.message = message

class ConfigError(Exception):
    def __init__(self, message):
        self.message = message

class DBError(Exception):
    def __init__(self, message):
        self.message = message

class AuthError(Exception):
     def __init__(self, message):
        self.message = message