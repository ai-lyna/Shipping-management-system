import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Vehicule
from django.core.paginator import Paginator

def vehicule_info(request):
    return JsonResponse({
        "numImmat": "string",
        "type_vehicule": "string",
        "capacitePoids": "number",
        "capaciteVolume": "number",
        "consommationCarburant": "number",
        "disponibilite": "boolean",
    })


def vehicule_data(request):
    table_fields = ["numImmat", "type_vehicule", "capacitePoids", "capaciteVolume", "disponibilite"]

    search_value = "" 
    vehs = Vehicule.objects.all().order_by("id")  

    if 'search' in request.GET:
        search_value = request.GET['search']
        if search_value:  
            vehs = Vehicule.objects.filter(numImmat__icontains=search_value)

    sort_order = request.GET.get('sort', 'new')  

    if sort_order == 'old':
        vehs = vehs.order_by('id')  
    else:
        vehs = vehs.order_by('-id')  

    paginator = Paginator(vehs, 12) 
    page_nbr = request.GET.get("page") 
    page_obj = paginator.get_page(page_nbr) 

    all_data = [
        {
            "id": v.id,
            "numImmat": v.numImmat,
            "type_vehicule": v.type_vehicule,
            "capacitePoids": v.capacitePoids,
            "capaciteVolume": v.capaciteVolume,
            "disponibilite": v.disponibilite,
        } for v in page_obj.object_list
    ]

    return render(request, 'pages/main.html', {
        "page_obj": page_obj, 
        "vehicules": page_obj, 
        "table_name": "Vehicules", 
        "data_structure": all_data, 
        "headers": table_fields, 
        "sort_order": sort_order,
        "query": search_value
    })


def vehicule_id_view(request, vehicule_id):
    try:
        vehicule = Vehicule.objects.get(id=vehicule_id)
        data = {
            "id": vehicule.id,
            "numImmat": vehicule.numImmat,
            "type_vehicule": vehicule.type_vehicule,
            "capacitePoids": vehicule.capacitePoids,
            "capaciteVolume": vehicule.capaciteVolume,
            "consommationCarburant": vehicule.consommationCarburant,
            "disponibilite": vehicule.disponibilite,
        }
        return JsonResponse(data)
    except Vehicule.DoesNotExist:
        return JsonResponse({"error": "Vehicule not found"}, status=404)
    
    
def update_vehicule(request, vehicule_id):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            vehicule = Vehicule.objects.get(id=vehicule_id)
            vehicule.numImmat = data.get("numImmat", vehicule.numImmat)
            vehicule.type_vehicule = data.get("type_vehicule", vehicule.type_vehicule)
            vehicule.capacitePoids = data.get("capacitePoids", vehicule.capacitePoids)
            vehicule.capaciteVolume = data.get("capaciteVolume", vehicule.capaciteVolume)
            vehicule.consommationCarburant = data.get("consommationCarburant", vehicule.consommationCarburant)
            if "disponibilite" in data:
                vehicule.disponibilite = data["disponibilite"]
            vehicule.save()
            
            return JsonResponse({
                "id": vehicule.id,
                "numImmat": vehicule.numImmat,
                "type_vehicule": vehicule.type_vehicule,
                "capacitePoids": vehicule.capacitePoids,
                "capaciteVolume": vehicule.capaciteVolume,
                "consommationCarburant": vehicule.consommationCarburant,
                "disponibilite": vehicule.disponibilite,
            })
        except Vehicule.DoesNotExist:
            return JsonResponse({"error": "Vehicule not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)


def create_vehicule(request):
    if request.method == "POST":
        data = json.loads(request.body)

        vehicule = Vehicule.objects.create(
            numImmat=data.get("numImmat"),
            type_vehicule=data.get("type_vehicule"),
            capacitePoids=data.get("capacitePoids", 0),
            capaciteVolume=data.get("capaciteVolume", 0),
            consommationCarburant=data.get("consommationCarburant", 0),
            disponibilite=data.get("disponibilite", True)
        )

        return JsonResponse({
            "id": vehicule.id,
            "numImmat": vehicule.numImmat,
            "type_vehicule": vehicule.type_vehicule,
            "capacitePoids": vehicule.capacitePoids,
            "capaciteVolume": vehicule.capaciteVolume,
            "consommationCarburant": vehicule.consommationCarburant,
            "disponibilite": vehicule.disponibilite,
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


def delete_vehicule(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        ids = data.get("ids", [])
        Vehicule.objects.filter(id__in=ids).delete()
        return JsonResponse({"msg":"vehicules deleted"})
    return JsonResponse({"error": "Invalid request"}, status=400)