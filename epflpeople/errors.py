class NoResultError(Exception):
    def __init__(self, search):
        self.search = search
        super(NoResultError, self).__init__(str(self))

    def __str__(self):
        return f"No results for '{self.search}'"


class ServiceNotResponding(Exception):
    def __init__(self):
        self.msg = 'External service not responding'
        super(ServiceNotResponding, self).__init__(self.msg)

    def __str__(self):
        return self.msg
