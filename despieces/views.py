from django.shortcuts import render


def custom_page_not_found_view(request, exception):
    return render(request, 'home/errors/404.html', status=404)


def custom_error_view(request, exception=None):
    return render(request, "home/errors/500.html", status=500)

