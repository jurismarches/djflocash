def get_ip_address(request):
    ip = ""
    try:
        info = dict(
            v.split("=")
            for v in request.META["HTTP_FORWARDED"].split(",")[0].split(";")
            if "=" in v
        )
        ip = info.get("for", "")
    except KeyError:
        pass
    if not ip:
        try:
            ip = request.META["HTTP_X_FORWARDED_FOR"].split(",")[0]
        except KeyError:
            pass
    if not ip:
        ip = request.META["REMOTE_ADDR"]
    return ip
