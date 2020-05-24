from django.http import JsonResponse


def dict_to_json(state="success", messages="访问提交成功", *args, **kwargs):
    my_data = {
        "state": state,
        "messages": messages,
    }
    if args:
        my_data.update(args)
    elif kwargs:
        my_data.update(kwargs)
    return JsonResponse(my_data, charset='utf-8', safe=False, json_dumps_params={'ensure_ascii': False})
