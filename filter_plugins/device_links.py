def search(devices, input):
    pass


def including(devices, input):
    pass


def excluding(devices, input):
    pass


class FilterModule(object):
    def filters(self):
        return {
            "including": including,
            "excluding": excluding,
        }
