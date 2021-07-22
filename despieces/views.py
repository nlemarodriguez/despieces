from django.shortcuts import render


def custom_page_not_found_view(request, exception):
    return render(request, 'errors/404.html', status=404)


def custom_error_view(request, exception=None):
    return render(request, "errors/500.html", status=500)


def custom_permission_view(request, exception=None):
    return render(request, "errors/403.html", status=403)

