from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .services.analytics_service_clean import DashboardCalculator


@csrf_exempt
@require_GET
def commercial_analysis(request):
    try:
        period_months = int(request.GET.get('period', 12))
        
        data = DashboardCalculator.get_commercial_analysis(period_months)
        
        return JsonResponse({
            'success': True,
            'data': data,
            'period': f"{period_months} mois"
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'data': None
        }, status=500)


@csrf_exempt
@require_GET
def operational_analysis(request):
    try:
        period_months = int(request.GET.get('period', 12))
        
        data = DashboardCalculator.get_operational_analysis(period_months)
        
        return JsonResponse({
            'success': True,
            'data': data,
            'period': f"{period_months} mois"
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'data': None
        }, status=500)


def dashboard(request , tab=None):
    """
    Dashboard view that handles both commercial and operational tabs
    based on the ?tab= query parameter.
    """
    # Determine active tab from query param, default to 'commercial'
    active_tab = request.GET.get('tab', 'commercial')

    context = {'active_tab': active_tab}

    if active_tab == 'commercial':
        commercial_data = DashboardCalculator.get_commercial_analysis()
        context.update({
            'expedition_change': commercial_data['expedition_change'],
            'revenue_change': commercial_data['revenue_change'],
            'monthly_trends': commercial_data['monthly_trends'],
            'top_clients': commercial_data['top_clients'],
            'top_destinations': commercial_data['top_destinations'],
        })

    elif active_tab == 'operational':
        operational_data = DashboardCalculator.get_operational_analysis()
        context.update({
            'tour_evolution': operational_data['tour_evolution'],
            'delivery_success': operational_data['delivery_success'],
            'tours_per_month': operational_data['tours_per_month'],
            'incident_zones': operational_data['incident_zones'],
            'peak_activity': operational_data['peak_activity'],
        })

    return render(request, 'pages/dashboard.html', context)



@csrf_exempt
@require_GET
def realtime_metrics(request):
    try:
        data = DashboardCalculator.get_realtime_metrics()
        
        return JsonResponse({
            'success': True,
            'data': data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'data': None
        }, status=500)


from django.utils import timezone