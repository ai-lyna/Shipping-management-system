import json
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Tarification
from backend.manageDestination.models import Destination
from backend.typeservice.models import TypeService



def tarification_info(request):
    return JsonResponse({
        "destination": "number",
        "service": "number",
        "tarifPoids": "number",
        "tarifVolume": "number",
    })




def tarification_data(request):

    table_fields = ["destination", "service", "tarifPoids", "tarifVolume"]

    tarifs = Tarification.objects.select_related("destination", "service").order_by("id")

    paginator = Paginator(tarifs, 12)
    page_nbr = request.GET.get("page")
    page_obj = paginator.get_page(page_nbr)

    all_data = [
        {
            "id": t.id,
            "destination": t.destination.ville,
            "service": t.service.typeService,
            "tarifPoids": str(t.tarifPoids),
            "tarifVolume": str(t.tarifVolume),
        }
        for t in page_obj.object_list
    ]

    return render(
        request,
        "pages/main.html",
        {
            "page_obj": page_obj,
            "tarifications": page_obj,
            "table_name": "Tarifications",
            "data_structure": all_data,
            "headers": table_fields,
        }
    )


def tarification_id_view(request, tarification_id):
    try:
        t = Tarification.objects.get(id=tarification_id)

        return JsonResponse({
            "id": t.id,
            "destination": t.destination.id,
            "destination_label": t.destination.ville,
            "service": t.service.id,
            "service_label": t.service.typeService,
            "tarifPoids": str(t.tarifPoids),
            "tarifVolume": str(t.tarifVolume),
        })

    except Tarification.DoesNotExist:
        return JsonResponse({"error": "Tarification not found"}, status=404)




def create_tarification(request):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            destination = Destination.objects.get(id=data.get("destination"))
            service = TypeService.objects.get(id=data.get("service"))

            tarification = Tarification.objects.create(
                destination=destination,
                service=service,
                tarifPoids=data.get("tarifPoids"),
                tarifVolume=data.get("tarifVolume"),
            )

            return JsonResponse({
                "id": tarification.id,
                "destination": destination.ville,
                "service": service.typeService,
                "tarifPoids": str(tarification.tarifPoids),
                "tarifVolume": str(tarification.tarifVolume),
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)




def update_tarification(request, tarification_id):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            t = Tarification.objects.get(id=tarification_id)

            if "destination" in data:
                t.destination = Destination.objects.get(id=data["destination"])

            if "service" in data:
                t.service = TypeService.objects.get(id=data["service"])

            t.tarifPoids = data.get("tarifPoids", t.tarifPoids)
            t.tarifVolume = data.get("tarifVolume", t.tarifVolume)

            t.save()

            return JsonResponse({
                "id": t.id,
                "destination": t.destination.ville,
                "service": t.service.typeService,
                "tarifPoids": str(t.tarifPoids),
                "tarifVolume": str(t.tarifVolume),
            })

        except Tarification.DoesNotExist:
            return JsonResponse({"error": "Tarification not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)




def delete_tarifications(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        ids = data.get("ids", [])

        Tarification.objects.filter(id__in=ids).delete()

        return JsonResponse({"msg": "tarifications deleted"})

    return JsonResponse({"error": "Invalid request"}, status=400)
