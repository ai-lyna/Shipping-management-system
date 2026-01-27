import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import TypeService
from django.core.paginator import Paginator


def typeservice_info(request):
    return JsonResponse({
        "typeService": {
            "type": "choice",
            "choices": [
                {"value": "standard", "label": "Standard"},
                {"value": "express", "label": "Express"},
                {"value": "urgent", "label": "Urgent"}
            ]
        },
        "Delai": "string",
    })


def typeservice_data(request):
    table_fields = ["typeService", "Delai"]
    
    search_value = ""
    services = TypeService.objects.all().order_by("id") 

    if 'search' in request.GET:
        search_value = request.GET['search']
        if search_value:
            services = TypeService.objects.filter(typeService__istartswith=search_value)

    sort_order = request.GET.get('sort', 'new')

    if sort_order == 'old':
        services = services.order_by('id')
    else:
        services = services.order_by('-id')

    paginator = Paginator(services, 12)
    page_nbr = request.GET.get("page")
    page_obj = paginator.get_page(page_nbr)

    all_data = [
        {
            "id": s.id,
            "typeService": s.typeService,
            "Delai": s.Delai,
        } for s in page_obj.object_list
    ]

    return render(request, 'pages/main.html', {
        "page_obj": page_obj,
        "typeservices": page_obj,
        "table_name": "Typeservice",
        "data_structure": all_data,
        "headers": table_fields,
        "sort_order": sort_order,
        "query": search_value
    })


def typeservice_id_view(request, service_id):
    try:
        service = TypeService.objects.get(id=service_id)
        data = {
            "id": service.id,
            "typeService": service.typeService,
            "Delai": service.Delai,
        }
        return JsonResponse(data)
    except TypeService.DoesNotExist:
        return JsonResponse({"error": "TypeService not found"}, status=404)


def update_typeservice(request, service_id):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            service = TypeService.objects.get(id=service_id)
            service.typeService = data.get("typeService", service.typeService)
            service.Delai = data.get("Delai", service.Delai)
            service.save()
            
            return JsonResponse({
                "id": service.id,
                "typeService": service.typeService,
                "Delai": service.Delai,
            })
        except TypeService.DoesNotExist:
            return JsonResponse({"error": "TypeService not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)


def create_typeservice(request):
    if request.method == "POST":
        data = json.loads(request.body)

        service = TypeService.objects.create(
            typeService=data.get("typeService"),
            Delai=data.get("Delai")
        )

        return JsonResponse({
            "id": service.id,
            "typeService": service.typeService,
            "Delai": service.Delai,
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


def delete_typeservices(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        ids = data.get("ids", [])
        TypeService.objects.filter(id__in=ids).delete()
        return JsonResponse({"msg": "typeservices deleted"})
    return JsonResponse({"error": "Invalid request"}, status=400)