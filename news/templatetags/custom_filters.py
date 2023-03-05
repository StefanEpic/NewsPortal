from django import template

register = template.Library()


@register.filter()
def censor(value):
    censor_words = ['хранилищ', 'актер', 'банк']
    result = []
    try:
        for i in value.split():
            app = True
            for j in censor_words:
                if j in i.lower():
                    result.append(i[0] + '*' * (len(i) - 1))
                    app = False
            if app:
                result.append(i)
        return " ".join(result)
    except AttributeError:
        return 'Error! Filter "censor" works only with strings!'
