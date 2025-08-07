class Registry:
    def __init__(self):
        self.commands = {}
        self.events = {}
        self.middleware = []

    def register_command(self, name, func):
        self.commands[name] = func

    def register_event(self, name, handler):
        self.events.setdefault(name, []).append(handler)

    def register_middleware(self, middleware_func):
        self.middleware.append(middleware_func)