from django.http import HttpResponse


async def some_view(request):
    return HttpResponse("I'm async view")
