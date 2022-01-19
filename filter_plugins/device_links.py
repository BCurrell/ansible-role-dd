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

    for link_type, devices in device_links.items():
        for device, links in devices.items():
            if device not in result:
                result[device] = {}
            if link_type not in result[device]:
                result[device][link_type] = []

            result[device][link_type] += links

    return result


def search(device_links, link):
    if link in device_links:
        return link

    for device, link_types in device_links.items():
        for link_type in link_types:
            if link in link_type:
                return device

    return None


def strip_paths(links):
    for link in links:
        yield link.split("/")[-1]


# TODO: This is horrible, there must be a better way
def including(device_links, links):
    for link in links:
        device = search(device_links, link)
        if device is not None:
            yield f"/dev/{device}"


# TODO: This is horrible, there must be a better way
def excluding(device_links, links):
    found = []

    for link in links:
        device = search(device_links, link)
        if device is not None:
            found += device

    for device in device_links:
        if device not in found:
            yield f"/dev/{device}"

class FilterModule(object):
    def filters(self):
        return {
            "reformat": reformat,
            "including": including,
            "excluding": excluding,
        }
