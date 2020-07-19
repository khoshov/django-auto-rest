from django.utils.text import slugify


def get_prefix(app, model):
    app_name = slugify(app.verbose_name.lower())
    model_name = model._meta.model_name
    return f'{app_name}/{model_name}'
