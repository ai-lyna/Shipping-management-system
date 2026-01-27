import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Colis
from django.core.paginator import Paginator


def colis_info(request):
    return JsonResponse({
        "poids": "number",
        "volume": "number",
        "description": "string",
        "expedition": "number",  
    })


def colis_data(request):
    table_fields = ["poids", "volume", "description", "expedition"]

    search_value = ""
    colis_list = Colis.objects.all().order_by("id")

    # Simple search by description
    if 'search' in request.GET:
        search_value = request.GET['search']
        if search_value:
            colis_list = Colis.objects.filter(description__istartswith=search_value)

    sort_order = request.GET.get('sort', 'new')
    if sort_order == 'old':
        colis_list = colis_list.order_by('id')  
    else:
        colis_list = colis_list.order_by('-id')

    paginator = Paginator(colis_list, 12)
    page_nbr = request.GET.get("page")
    page_obj = paginator.get_page(page_nbr)

    all_data = [
        {
            "id": c.id,
            "poids": c.poids,
            "volume": c.volume,
            "description": c.description,
            "expedition": c.expedition.id if c.expedition else None,
        } for c in page_obj.object_list
    ]

    return render(request, 'pages/main.html', {
        "page_obj": page_obj,
        "colis": page_obj,
        "table_name": "Colis",
        "data_structure": all_data,
        "headers": table_fields,
        "sort_order": sort_order,
        "query": search_value
    })



def colis_id_view(request, colis_id):
    try:
        c = Colis.objects.get(id=colis_id)
        data = {
            "id": c.id,
            "poids": c.poids,
            "volume": c.volume,
            "description": c.description,
            "expedition": c.expedition.id if c.expedition else None,
        }
        return JsonResponse(data)
    except Colis.DoesNotExist:
        return JsonResponse({"error": "Colis not found"}, status=404)



def update_colis(request, colis_id):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            c = Colis.objects.get(id=colis_id)
            c.poids = data.get("poids", c.poids)
            c.volume = data.get("volume", c.volume)
            c.description = data.get("description", c.description)
            expedition_id = data.get("expedition")
            if expedition_id:
                from backend.manageExpedition.models import Expedition
                c.expedition = Expedition.objects.get(id=expedition_id)
            c.save()

            return JsonResponse({
                "id": c.id,
                "poids": c.poids,
                "volume": c.volume,
                "description": c.description,
                "expedition": c.expedition.id if c.expedition else None,
            })
        except Colis.DoesNotExist:
            return JsonResponse({"error": "Colis not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)


def create_colis(request):
    if request.method == "POST":
        data = json.loads(request.body)
        from backend.manageExpedition.models import Expedition
        expedition = Expedition.objects.get(id=data.get("expedition")) if data.get("expedition") else None

        c = Colis.objects.create(
            poids=data.get("poids", 0),
            volume=data.get("volume", 0),
            description=data.get("description", ""),
            expedition=expedition
        )

        return JsonResponse({
            "id": c.id,
            "poids": c.poids,
            "volume": c.volume,
            "description": c.description,
            "expedition": c.expedition.id if c.expedition else None,
        })
    return JsonResponse({"error": "Invalid request"}, status=400)



def delete_colis(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        ids = data.get("ids", [])
        Colis.objects.filter(id__in=ids).delete()
        return JsonResponse({"msg": "colis deleted"})
    return JsonResponse({"error": "Invalid request"}, status=400)