import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Destination
from django.core.paginator import Paginator


def destination_info(request):
    return JsonResponse({
        "numBureau": "number",
        "ville": "string",
        "pays": "string",
        "zoneGeo": "string",
        "tarifBase": "number",
    })


def destination_data(request):

    table_fields = ["numBureau", "ville", "pays", "zoneGeo", "tarifBase"]
    
    search_value = "" 
    dests = Destination.objects.all().order_by("numBureau") 

    if 'search' in request.GET:
        search_value = request.GET['search']
        if search_value:  
            dests = Destination.objects.filter(ville__istartswith=search_value)

    sort_order = request.GET.get('sort', 'new')  

    if sort_order == 'old':
        dests = dests.order_by('numBureau')  
    else:
        dests = dests.order_by('-numBureau')  

    paginator = Paginator(dests, 12) 
    page_nbr = request.GET.get("page") 
    page_obj = paginator.get_page(page_nbr) 

    all_data = [
        {
            "id": d.numBureau,  
            "numBureau": d.numBureau,
            "ville": d.ville,
            "pays": d.pays,
            "zoneGeo": d.zoneGeo,
            "tarifBase": d.tarifBase,
        } for d in page_obj.object_list
    ]

    return render(request, 'pages/main.html', {
        "page_obj": page_obj,
        "destinations": page_obj,
        "table_name": "Destinations",
        "data_structure": all_data,
        "headers": table_fields,
        "sort_order": sort_order,
        "query": search_value
    })


def destination_id_view(request, numBureau):
    try:
        dest = Destination.objects.get(numBureau=numBureau)
        data = {
            "id": dest.numBureau,
            "numBureau": dest.numBureau,
            "ville": dest.ville,
            "pays": dest.pays,
            "zoneGeo": dest.zoneGeo,
            "tarifBase": dest.tarifBase,
        }
        return JsonResponse(data)
    except Destination.DoesNotExist:
        return JsonResponse({"error": "Destination not found"}, status=404)
    
    
def update_destination(request, numBureau):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            dest = Destination.objects.get(numBureau=numBureau)
            dest.ville = data.get("ville", dest.ville)
            dest.pays = data.get("pays", dest.pays)
            dest.zoneGeo = data.get("zoneGeo", dest.zoneGeo)
            dest.tarifBase = data.get("tarifBase", dest.tarifBase)
            dest.save()
            
            return JsonResponse({
                "id": dest.numBureau,
                "numBureau": dest.numBureau,
                "ville": dest.ville,
                "pays": dest.pays,
                "zoneGeo": dest.zoneGeo,
                "tarifBase": dest.tarifBase
            })
        except Destination.DoesNotExist:
            return JsonResponse({"error": "Destination not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)


def create_destination(request):
    if request.method == "POST":
        data = json.loads(request.body)

        dest = Destination.objects.create(
            numBureau=data.get("numBureau"),
            ville=data.get("ville"),
            pays=data.get("pays"),
            zoneGeo=data.get("zoneGeo"),
            tarifBase=data.get("tarifBase", 0)
        )

        return JsonResponse({
            "id": dest.numBureau,
            "numBureau": dest.numBureau,
            "ville": dest.ville,
            "pays": dest.pays,
            "zoneGeo": dest.zoneGeo,
            "tarifBase": dest.tarifBase
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


def delete_destinations(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        ids = data.get("ids", [])
        Destination.objects.filter(numBureau__in=ids).delete()
        return JsonResponse({"msg":"destinations deleted"})
    return JsonResponse({"error": "Invalid request"}, status=400)