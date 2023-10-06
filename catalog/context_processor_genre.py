from catalog import models


def genre(request):
    return {'genres': models.Genre(request)}