class ClientIPMiddleware:
    """
    request.client_ip を付与
    ※ もしリバプロ配下なら X-Forwarded-For を厳密運用に変える
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR", "") or "0.0.0.0"
        request.client_ip = ip
        return self.get_response(request)
