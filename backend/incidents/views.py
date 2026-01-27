import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Incident
from django.core.paginator import Paginator

def incident_info(request):
    return JsonResponse({
    "incident_type": {
        "type": "choice",
        "choices": [
            {"value": "retard", "label": "Retard"},
            {"value": "perte", "label": "Perte"},
            {"value": "dommage", "label": "Dommage"},
            {"value": "technique", "label": "Problème technique"},
            {"value": "autre", "label": "Autre"}
        ]
    },
    "tour_id": "number",
    "description": "string",
    "date_reported": "string",
    "resolu": "boolean",
    "trajet": "number",
    })


def incident_data(request):

    table_fields = ["incident_type", "tour", "description", "date_reported", "resolu"]
    
    search_value = ""
    incidents = Incident.objects.all().order_by("id")

    if 'search' in request.GET:
        search_value = request.GET['search']
        if search_value:
            incidents = incidents.filter(description__icontains=search_value)

    sort_order = request.GET.get('sort', 'new')

    if sort_order == 'old':
        incidents = incidents.order_by('date_reported')
    else:
        incidents = incidents.order_by('-date_reported')

    paginator = Paginator(incidents, 12)
    page_nbr = request.GET.get("page")
    page_obj = paginator.get_page(page_nbr)

    all_data = [
        {
            "id": i.id,
            "incident_type": i.incident_type,
            "tour": i.tour.id if i.tour else None,
            "description": i.description,
            "date_reported": i.date_reported.strftime("%Y-%m-%d %H:%M"),
            "resolu": i.resolu,
        } for i in page_obj.object_list
    ]

    return render(request, 'pages/main.html', {
        "page_obj": page_obj,
        "incidents": page_obj,
        "table_name": "Incidents",
        "data_structure": all_data,
        "headers": table_fields,
        "sort_order": sort_order,
        "query": search_value
    })


def incident_id_view(request, incident_id):
    try:
        incident = Incident.objects.get(id=incident_id)
        data = {
            "id": incident.id,
            "incident_type": incident.incident_type,
            "tour": incident.tour.id if incident.tour else None,
            "description": incident.description,
            "date_reported": incident.date_reported.strftime("%Y-%m-%d %H:%M"),
            "resolu": incident.resolu,
            "trajet": incident.trajet.id if incident.trajet else None,
        }
        return JsonResponse(data)
    except Incident.DoesNotExist:
        return JsonResponse({"error": "Incident not found"}, status=404)


def update_incident(request, incident_id):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            incident = Incident.objects.get(id=incident_id)
            incident.incident_type = data.get("incident_type", incident.incident_type)
            incident.description = data.get("description", incident.description)
            incident.resolu = data.get("resolu", incident.resolu)
            incident.trajet_id = data.get("trajet", incident.trajet_id)
            # Updating tour if provided
            tour_id = data.get("tour_id")
            if tour_id is not None:
                from backend.manageExpedition.models import Tournée
                try:
                    incident.tour = Tournée.objects.get(id=tour_id)
                except Tournée.DoesNotExist:
                    incident.tour = None
            incident.save()
            
            return JsonResponse({
                "id": incident.id,
                "incident_type": incident.incident_type,
                "tour": incident.tour.id if incident.tour else None,
                "description": incident.description,
                "date_reported": incident.date_reported.strftime("%Y-%m-%d %H:%M"),
                "resolu": incident.resolu,
            })
        except Incident.DoesNotExist:
            return JsonResponse({"error": "Incident not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)


def create_incident(request):
    if request.method == "POST":
        data = json.loads(request.body)
        from backend.manageExpedition.models import Tournée

        tour = None
        tour_id = data.get("tour_id")
        if tour_id:
            try:
                tour = Tournée.objects.get(id=tour_id)
            except Tournée.DoesNotExist:
                tour = None

        incident = Incident.objects.create(
            incident_type=data.get("incident_type"),
            description=data.get("description"),
            resolu=data.get("resolu", False),
            tour=tour,
            trajet_id=data.get("trajet"),
        )

        return JsonResponse({
            "id": incident.id,
            "incident_type": incident.incident_type,
            "tour": incident.tour.id if incident.tour else None,
            "description": incident.description,
            "date_reported": incident.date_reported.strftime("%Y-%m-%d %H:%M"),
            "resolu": incident.resolu,
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


def delete_incidents(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        ids = data.get("ids", [])
        Incident.objects.filter(id__in=ids).delete()
        return JsonResponse({"msg": "incidents deleted"})
    return JsonResponse({"error": "Invalid request"}, status=400)