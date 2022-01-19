def args(d, delimitor="=", joiner=" "):
    result = []

    for k,v in d.items():
        result += f"{k}{delimitor}{v}"

    return joiner.join(result)


class FilterModule(object):

    def filters():
        return {
            "args": args,
        }
