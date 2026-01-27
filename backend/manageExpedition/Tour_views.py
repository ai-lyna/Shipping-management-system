import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Tournee
from django.core.paginator import Paginator


def tournee_info(request):
    return JsonResponse({
        "dateTourne": "YYYY-MM-DD",
        "id_chauff": "number",
        "id_vehicule": "number",
        "numBureau": "list of numBureau",
    })


def tournee_data(request):

    table_fields = ["dateTourne", "id_chauff", "id_vehicule", "numBureau"]
    
    search_value = "" 
    tournees = Tournee.objects.all().order_by("id") 

    if 'search' in request.GET:
        search_value = request.GET['search']
        if search_value:  
            tournees = Tournee.objects.filter(id_chauff__nom__istartswith=search_value)

    sort_order = request.GET.get('sort', 'new')  

    if sort_order == 'old':
        tournees = tournees.order_by('id')  
    else:
        tournees = tournees.order_by('-id')  

    paginator = Paginator(tournees, 12) 
    page_nbr = request.GET.get("page") 
    page_obj = paginator.get_page(page_nbr) 

    all_data = [
        {
            "id": t.id,
            "dateTourne": t.dateTourne.strftime("%Y-%m-%d"),
            "id_chauff": t.id_chauff.id if t.id_chauff else None,
            "id_vehicule": t.id_vehicule.id if t.id_vehicule else None,
            "numBureau": [d.numBureau for d in t.numBureau.all()],
        } for t in page_obj.object_list
    ]

    return render(request, 'pages/main.html', {
        "page_obj": page_obj,
        "tournees": page_obj,
        "table_name": "Tournees",
        "data_structure": all_data,
        "headers": table_fields,
        "sort_order": sort_order,
        "query": search_value
    })


def tournee_id_view(request, tournee_id):
    try:
        t = Tournee.objects.get(id=tournee_id)
        data = {
            "id": t.id,
            "dateTourne": t.dateTourne.strftime("%Y-%m-%d"),
            "id_chauff": t.id_chauff.id if t.id_chauff else None,
            "id_vehicule": t.id_vehicule.id if t.id_vehicule else None,
            "numBureau": [d.numBureau for d in t.numBureau.all()],
        }
        return JsonResponse(data)
    except Tournee.DoesNotExist:
        return JsonResponse({"error": "Tournée not found"}, status=404)
    
    
def update_tournee(request, tournee_id):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            t = Tournee.objects.get(id=tournee_id)
            t.dateTourne = data.get("dateTourne", t.dateTourne)
            
            if "id_chauff" in data:
                from backend.logistics.models import Chauffeur
                t.id_chauff = Chauffeur.objects.get(id=data["id_chauff"])
            if "id_vehicule" in data:
                from backend.logistics.models import Vehicule
                t.id_vehicule = Vehicule.objects.get(id=data["id_vehicule"])
            if "numBureau" in data:
                from backend.manageDestination.models import Destination
                t.numBureau.set(Destination.objects.filter(numBureau__in=data["numBureau"]))
            t.save()
            
            return JsonResponse({
                "id": t.id,
                "dateTourne": t.dateTourne.strftime("%Y-%m-%d"),
                "id_chauff": t.id_chauff.id if t.id_chauff else None,
                "id_vehicule": t.id_vehicule.id if t.id_vehicule else None,
                "numBureau": [d.numBureau for d in t.numBureau.all()],
            })
        except Tournee.DoesNotExist:
            return JsonResponse({"error": "Tournée not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)


def create_tournee(request):
    if request.method == "POST":
        data = json.loads(request.body)

        from backend.logistics.models import Chauffeur, Vehicule
        from backend.manageDestination.models import Destination

        t = Tournee.objects.create(
            dateTourne=data.get("dateTourne"),
            id_chauff=Chauffeur.objects.get(id=data.get("id_chauff")) if data.get("id_chauff") else None,
            id_vehicule=Vehicule.objects.get(id=data.get("id_vehicule")) if data.get("id_vehicule") else None,
        )
        if "numBureau" in data:
            t.numBureau.set(Destination.objects.filter(numBureau__in=data["numBureau"]))
            t.save()

        return JsonResponse({
            "id": t.id,
            "dateTourne": t.dateTourne.strftime("%Y-%m-%d"),
            "id_chauff": t.id_chauff.id if t.id_chauff else None,
            "id_vehicule": t.id_vehicule.id if t.id_vehicule else None,
            "numBureau": [d.numBureau for d in t.numBureau.all()],
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


def delete_tournees(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        ids = data.get("ids", [])
        Tournee.objects.filter(id__in=ids).delete()
        return JsonResponse({"msg": "tournees deleted"})
    return JsonResponse({"error": "Invalid request"}, status=400)