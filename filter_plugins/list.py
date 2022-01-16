def including(input, filter):
    return input

def excluding(input, filter):
    return input

class FilterModule(object):

    def filters(self):
        return {
            'including': including,
            'excluding': excluding,
        }
