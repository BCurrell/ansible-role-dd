def reformat(device_links):
    """
    Ansible format:
    "ids": {
        "sda": []
    },
    "labels": {
        "sda": []
    },
    "ids": {
        "sda": []
    }

    Reformat:
    "sda": {
        "ids": [],
        "labels": [],
        "uuids": []
    }
    """
    result = {}

    for link, devices in device_links.items():
        for device, links in devices.items():
            if device not in result:
                result[device] = {}
            if link not in result[device]:
                result[device][link] = []

            result[device][link] += links

    return result


def search(device_links, val, do_reformat=False):
    if do_reformat:
        device_links = reformat(device_links)
    
    if val in device_links:
        return val

    for device, links in device_links.items():
        for link in links:
            if val in link:
                return val

    return None


def including(device_links, input):
    pass


def excluding(device_links, input):
    pass


class FilterModule(object):
    def filters(self):
        return {
            "reformat": reformat,
            "including": including,
            "excluding": excluding,
        }
