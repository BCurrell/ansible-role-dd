def nested_get(input, key):
    if isinstance(key, str):
        key = key.split(".")

    k0 = key.pop(0)

    if k0 not in input:
        return None

    if len(key) == 0:
        return input.get(k0)
    else:
        return nested_get(input.get(k0), key)


def filter(devices, key, value, invert=False):
    """
    This would be better as a generator, but it gets messy when using dicts,
    and I've not yet run down how Ansible facts handle being generators.
    """
    result = {}

    for dpath, device in devices.items():
        v0 = nested_get(device, key)

        if v0 is None:
            continue

        if not invert and v0 == value:
            result[dpath] = device
        elif invert and v0 != value:
            result[dpath] = device

    return result


def removable(devices, invert=False):
    return filter(devices, "removable", "1", invert)


def sectors(devices, value="0", invert=False):
    return filter(devices, "sectors", value, invert)


def valid_storage(devices):
    return removable(sectors(devices, "0", True), True)


def partitions(devices, include_parent=False):
    """
    This would be better as a generator, but it gets messy when using dicts,
    and I've not yet run down how Ansible facts handle being generators.
    """
    result = {}

    for dpath, device in devices.items():
        if include_parent:
            result[dpath] = device

        # TODO: Maybe replace .get with .pop to prevent multiple calls to partitions causing issues
        for ppath, partition in device.get("partitions").items():
            result[ppath] = partition

    return result


def paths(devices):
    for device in devices:
        yield f"/dev/{device}"


class FilterModule(object):
    def filters(self):
        return {
            "partitions": partitions,
            "paths": paths,
            "removable": removable,
            "sectors": sectors,
            "valid_storage": valid_storage,
        }
