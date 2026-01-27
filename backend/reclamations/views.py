import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Reclamation
from django.core.paginator import Paginator


def reclamation_info(request):
    return JsonResponse({
        "client_id": "number",
        "incident_id": "number or null",
        "expedition_id": "number or null",
        "facture_id": "number or null",
        "objet": "string",
        "description": "string",
        "date_reclamation": "datetime string",
        "statut": {
            "type": "choice",
            "choices": [
                {"value": "en_cours", "label": "En cours"},
                {"value": "resolue", "label": "Résolue"},
                {"value": "annulee", "label": "Annulée"},
            ]
        }
    })


def reclamation_data(request):
    table_fields = ["client", "incident", "expedition", "facture", "objet", "statut"]
    
    search_value = ""
    recs = Reclamation.objects.all().order_by("-id")

    if 'search' in request.GET:
        search_value = request.GET['search']
        if search_value:
            recs = recs.filter(objet__icontains=search_value)

    sort_order = request.GET.get('sort', 'new')
    if sort_order == 'old':
        recs = recs.order_by('date_reclamation')
    else:
        recs = recs.order_by('-date_reclamation')

    paginator = Paginator(recs, 12)
    page_nbr = request.GET.get("page")
    page_obj = paginator.get_page(page_nbr)

    all_data = [
        {
            "id": r.id,
            "client": r.client.nom,
            "incident": r.incident.id if r.incident else None,
            "expedition": r.expedition.id if r.expedition else None,
            "facture": r.facture.id if r.facture else None,
            "objet": r.objet,
            "statut": r.statut
        } for r in page_obj.object_list
    ]

    return render(request, 'pages/main.html', {
        "page_obj": page_obj,
        "reclamations": page_obj,
        "table_name": "Reclamations",
        "data_structure": all_data,
        "headers": table_fields,
        "sort_order": sort_order,
        "query": search_value
    })



def reclamation_id_view(request, reclamation_id):
    try:
        r = Reclamation.objects.get(id=reclamation_id)
        data = {
            "id": r.id,
            "client": r.client.nom,
            "incident": r.incident.id if r.incident else None,
            "expedition": r.expedition.id if r.expedition else None,
            "facture": r.facture.id if r.facture else None,
            "objet": r.objet,
            "description": r.description,
            "date_reclamation": r.date_reclamation.strftime("%Y-%m-%d %H:%M"),
            "statut": r.statut
        }
        return JsonResponse(data)
    except Reclamation.DoesNotExist:
        return JsonResponse({"error": "Reclamation not found"}, status=404)



def create_reclamation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        r = Reclamation.objects.create(
            client_id=data.get("client_id"),
            incident_id=data.get("incident_id"),
            expedition_id=data.get("expedition_id"),
            facture_id=data.get("facture_id"),
            objet=data.get("objet"),
            description=data.get("description"),
            statut=data.get("statut", "en_cours")
        )

        return JsonResponse({
            "id": r.id,
            "client": r.client.id if r.client else None,
            "incident": r.incident.id if r.incident else None,
            "expedition": r.expedition.id if r.expedition else None,
            "facture": r.facture.id if r.facture else None,
            "objet": r.objet,
            "statut": r.statut
        })

    return JsonResponse({"error": "Invalid request"}, status=400)



def update_reclamation(request, reclamation_id):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            r = Reclamation.objects.get(id=reclamation_id)
            r.client_id = data.get("client_id", r.client_id)
            r.incident_id = data.get("incident_id", r.incident_id)
            r.expedition_id = data.get("expedition_id", r.expedition_id)
            r.facture_id = data.get("facture_id", r.facture_id)
            r.objet = data.get("objet", r.objet)
            r.description = data.get("description", r.description)
            r.statut = data.get("statut", r.statut)
            r.save()

            return JsonResponse({
                "id": r.id,
                "client": r.client.nom,
                "incident": r.incident.id if r.incident else None,
                "expedition": r.expedition.id if r.expedition else None,
                "facture": r.facture.id if r.facture else None,
                "objet": r.objet,
                "statut": r.statut
            })
        except Reclamation.DoesNotExist:
            return JsonResponse({"error": "Reclamation not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)



def delete_reclamations(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        ids = data.get("ids", [])
        Reclamation.objects.filter(id__in=ids).delete()
        return JsonResponse({"msg": "reclamations deleted"})
    return JsonResponse({"error": "Invalid request"}, status=400)