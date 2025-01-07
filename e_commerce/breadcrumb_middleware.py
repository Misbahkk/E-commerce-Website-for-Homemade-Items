# middleware/breadcrumb_middleware.py

class BreadcrumbMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Split the URL path into segments
        path_segments = request.path.strip('/').split('/')

        # Construct breadcrumbs
        breadcrumbs = []
        cumulative_path = ""
        for segment in path_segments:
            cumulative_path += f"/{segment}"
            if segment:
                breadcrumbs.append({
                    "name": segment.capitalize(),
                    "url": cumulative_path
                })

        # Add breadcrumb data to the request
        request.breadcrumbs = breadcrumbs
        return self.get_response(request)
