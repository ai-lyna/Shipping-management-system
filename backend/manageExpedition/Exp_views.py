import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Expedition
from django.core.paginator import Paginator


def expedition_info(request):
    return JsonResponse({
        "client": "number",
        "statut": "string",
        "numBureau": "number",
        "tournee": "number",
        "type_service": "number",
    })


def expedition_data(request):

    table_fields = ["client" , "statut",  "numBureau", "tournee"]
    
    search_value = "" 
    exps = Expedition.objects.all().order_by("id_Exp") 

    if 'search' in request.GET:
        search_value = request.GET['search']
        if search_value:  
            exps = Expedition.objects.filter(client__nom__istartswith=search_value)

    sort_order = request.GET.get('sort', 'new')  

    if sort_order == 'old':
        exps = exps.order_by('id_Exp')  
    else:
        exps = exps.order_by('-id_Exp')  

    paginator = Paginator(exps, 12) 
    page_nbr = request.GET.get("page") 
    page_obj = paginator.get_page(page_nbr) 

    all_data = [
        {
            "id": e.id,
            "client": e.client.id,
            "statut": e.statut,
            "numBureau": e.numBureau.numBureau,
            "tournee": e.tournee.id if e.tournee else None,
         
        } for e in page_obj.object_list
    ]

    return render(request, 'pages/main.html', {
        "page_obj": page_obj,
        "expeditions": page_obj,
        "table_name": "Expeditions",
        "data_structure": all_data,
        "headers": table_fields,
        "sort_order": sort_order,
        "query": search_value
    })


def expedition_id_view(request, expedition_id):
    try:
        e = Expedition.objects.get(id_Exp=expedition_id)
        data = {
            "id": e.id_Exp,
            "client": e.client.id,
            "type_service": e.type_service.id if e.type_service else None,
            "statut": e.statut,
            "date_exped": e.date_exped.strftime("%Y-%m-%d %H:%M"),
            "numBureau": e.numBureau.numBureau,
            "tournee": e.tournee.id if e.tournee else None,
         
        }
        return JsonResponse(data)
    except Expedition.DoesNotExist:
        return JsonResponse({"error": "Expedition not found"}, status=404)
    
    
def update_expedition(request, expedition_id):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            e = Expedition.objects.get(id=expedition_id)
            from backend.clients.models import Client
            from backend.typeservice.models import Typetype_service
            from backend.manageDestination.models import Destination
            from backend.manageExpedition.models import Tournée

            if "client" in data:
                e.client = Client.objects.get(id=data["client"])
            if "type_service" in data:
                e.type_service = Typetype_service.objects.get(id=data["type_service"])
            if "statut" in data:
                e.statut = data["statut"]
            if "numBureau" in data:
                e.numBureau = Destination.objects.get(numBureau=data["numBureau"])
            if "tournee" in data:
                e.tournee = Tournée.objects.get(id=data["tournee"])

            e.save()
            
            return JsonResponse({
                "id": e.id_Exp,
                "client": e.client.id,
                "statut": e.statut,
                "numBureau": e.numBureau.numBureau,
                "tournee": e.tournee.id if e.tournee else None,
           
            })
        except Expedition.DoesNotExist:
            return JsonResponse({"error": "Expedition not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)


def create_expedition(request):
    if request.method == "POST":
        data = json.loads(request.body)

        from backend.clients.models import Client
        from backend.typeservice.models import Typetype_service
        from backend.manageDestination.models import Destination
        from backend.manageExpedition.models import Tournée

        e = Expedition.objects.create(
            client=Client.objects.get(id=data.get("client")),
            type_service=Typetype_service.objects.get(id=data.get("type_service")) if data.get("type_service") else None,
            statut=data.get("statut"),
            numBureau=Destination.objects.get(numBureau=data.get("numBureau")),
            tournee=Tournée.objects.get(id=data.get("tournee")) if data.get("tournee") else None,
        )

        return JsonResponse({
            "id": e.id_Exp,
            "client": e.client.id,
            "statut": e.statut,
            "numBureau": e.numBureau.numBureau,
            "tournee": e.tournee.id if e.tournee else None,
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


def delete_expeditions(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        ids = data.get("ids", [])
        Expedition.objects.filter(id__in=ids).delete()
        return JsonResponse({"msg": "expeditions deleted"})
    return JsonResponse({"error": "Invalid request"}, status=400)