API_VERSION = "v1-alpha"

def versioned_path(path):
    return f"/api/{API_VERSION}/{path.strip('/')}"
