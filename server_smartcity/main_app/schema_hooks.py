def hide_delete_report_endpoints(endpoints):
    filtered = []

    for path, path_regex, method, callback in endpoints:
        method_name = str(method).upper()
        path_name = str(path)

        if method_name == 'DELETE' and path_name.startswith('/api/report'):
            continue

        filtered.append((path, path_regex, method, callback))

    return filtered