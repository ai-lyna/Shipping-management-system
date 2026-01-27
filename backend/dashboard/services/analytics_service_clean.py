from datetime import datetime, timedelta
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from backend.clients.models import Client
from backend.manageExpedition.models import Expedition, Tournee
from backend.logistics.models import Chauffeur
from backend.incidents.models import Incident

class DashboardCalculator:

    @staticmethod
    def get_commercial_analysis(period_months=12):
        expedition_change = DashboardCalculator._calculate_expedition_change(period_months)
        revenue_change = DashboardCalculator._calculate_revenue_change(period_months)
        top_clients = DashboardCalculator._get_top_clients(period_months)
        top_destinations = DashboardCalculator._get_top_destinations(period_months)
        monthly_trends = DashboardCalculator._get_monthly_expeditions_trend(period_months)

        return {
            'expedition_change': expedition_change,
            'revenue_change': revenue_change,
            'top_clients': top_clients,
            'top_destinations': top_destinations,
            'monthly_trends': monthly_trends,
            'period_months': period_months
        }

    @staticmethod
    def get_operational_analysis(period_months=12):
        tour_evolution = DashboardCalculator._calculate_tour_evolution(period_months)
        delivery_success = DashboardCalculator._calculate_delivery_success(period_months)
        top_drivers = DashboardCalculator._get_top_drivers(period_months)
        incident_zones = DashboardCalculator._get_incident_zones(period_months)
        peak_activity = DashboardCalculator._get_peak_activity_months(period_months)
        tours_per_month = DashboardCalculator._get_tours_per_month_chart(period_months)

        return {
            'tour_evolution': tour_evolution,
            'delivery_success': delivery_success,
            'top_drivers': top_drivers,
            'incident_zones': incident_zones,
            'peak_activity': peak_activity,
            'tours_per_month': tours_per_month,
            'period_months': period_months
        }

    @staticmethod
    def get_realtime_metrics():
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        stats = Expedition.objects.filter(date_exped__gte=today_start).aggregate(
            count=Count('id_Exp'),
            revenue=Sum('montant_total')
        )
        
        today_tours = Tournee.objects.filter(date_tournee__gte=today_start).count()
        today_incidents = Incident.objects.filter(date_reported__gte=today_start).count()
        
        active_tours = Tournee.objects.filter(statut='en_cours').count() if hasattr(Tournee, 'statut') else 0
        pending_expeditions = Expedition.objects.filter(statut='en_attente').count()

        return {
            'today': {
                'expeditions': stats['count'] or 0,
                'revenue': float(stats['revenue'] or 0),
                'tours': today_tours,
                'incidents': today_incidents
            },
            'ongoing': {
                'active_tours': active_tours,
                'pending_expeditions': pending_expeditions
            },
            'updated_at': now.isoformat()
        }

    @staticmethod
    def _calculate_expedition_change(period_months):
        end_date = timezone.now()
        current_start = end_date - timedelta(days=30 * period_months)
        current_count = Expedition.objects.filter(date_exped__gte=current_start).count()
        
        previous_start = current_start - timedelta(days=30 * period_months)
        previous_count = Expedition.objects.filter(date_exped__gte=previous_start, date_exped__lt=current_start).count()

        change_percent = ((current_count - previous_count) / previous_count * 100) if previous_count > 0 else 0
        return {
            'current_count': current_count,
            'previous_count': previous_count,
            'change_percent': round(change_percent, 1),
            'is_increase': change_percent >= 0,
            'label': f"{'+' if change_percent >= 0 else ''}{round(change_percent, 1)}%"
        }

    @staticmethod
    def _calculate_revenue_change(period_months):
        end_date = timezone.now()
        current_start = end_date - timedelta(days=30 * period_months)
        
        current_revenue = Expedition.objects.filter(date_exped__gte=current_start).aggregate(total=Sum('montant_total'))['total'] or 0
        previous_revenue = Expedition.objects.filter(date_exped__lt=current_start, date_exped__gte=current_start - timedelta(days=30*period_months)).aggregate(total=Sum('montant_total'))['total'] or 0

        change_percent = ((current_revenue - previous_revenue) / previous_revenue * 100) if previous_revenue > 0 else 0
        return {
            'current_revenue': float(current_revenue),
            'previous_revenue': float(previous_revenue),
            'change_percent': round(change_percent, 1),
            'is_increase': change_percent >= 0,
            'label': f"{'+' if change_percent >= 0 else ''}{round(change_percent, 1)}%"
        }

    @staticmethod
    def _get_top_clients(period_months, limit=7):
        start_date = timezone.now() - timedelta(days=30 * period_months)
        clients = Client.objects.filter(expeditions__date_exped__gte=start_date).distinct()
        clients_list = []
        for client in clients:
            total_value = client.expeditions.filter(date_exped__gte=start_date).aggregate(total=Sum('montant_total'))['total'] or 0
            expedition_count = client.expeditions.filter(date_exped__gte=start_date).count()
            clients_list.append({
                'name': f"{client.prenom} {client.nom}",
                'company': getattr(client, 'entreprise', "N/A"),
                'expedition_count': expedition_count,
                'total_value': float(total_value)
            })
        return sorted(clients_list, key=lambda x: x['total_value'], reverse=True)[:limit]

    @staticmethod
    def _get_top_destinations(period_months):
        start_date = timezone.now() - timedelta(days=period_months*30)
        destinations = Expedition.objects.filter(date_exped__gte=start_date).exclude(Q(numBureau__ville__isnull=True) | Q(numBureau__ville='')).values('numBureau__ville').annotate(count=Count('id_Exp')).order_by('-count')[:10]
        return [d['numBureau__ville'] for d in destinations], [d['count'] for d in destinations]

    @staticmethod
    def _get_monthly_expeditions_trend(period_months):
        start_date = timezone.now() - timedelta(days=30 * period_months)
        monthly_data = Expedition.objects.filter(date_exped__gte=start_date).annotate(month=TruncMonth('date_exped')).values('month').annotate(count=Count('id_Exp')).order_by('month')
        month_names_fr = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
        counts_dict = {entry['month'].strftime('%b'): entry['count'] for entry in monthly_data}
        return {'labels': month_names_fr, 'counts': [counts_dict.get(month, 0) for month in month_names_fr]}

    @staticmethod
    def _calculate_tour_evolution(period_months):
        end_date = timezone.now()
        current_start = end_date - timedelta(days=30 * period_months)
        current_count = Tournee.objects.filter(date_tournee__gte=current_start).count()
        previous_count = Tournee.objects.filter(date_tournee__lt=current_start, date_tournee__gte=current_start - timedelta(days=30*period_months)).count()
        change_percent = ((current_count - previous_count) / previous_count * 100) if previous_count > 0 else 0
        return {'current_count': current_count, 'previous_count': previous_count, 'change_percent': round(change_percent, 1), 'is_increase': change_percent >= 0}

    @staticmethod
    def _calculate_delivery_success(period_months):
        start_date = timezone.now() - timedelta(days=30 * period_months)
        stats = Expedition.objects.filter(date_exped__gte=start_date).aggregate(
            total=Count('id_Exp'),
            delivered=Count('id_Exp', filter=Q(statut='livr')),
            failed=Count('id_Exp', filter=Q(statut='echec')),
            delayed=Count('id_Exp', filter=Q(statut='encourslivr'))
        )
        total = stats['total'] or 0
        success_rate = (stats['delivered'] / total * 100) if total > 0 else 0
        return {
            'total': total or 1,
            'delivered': stats['delivered'],
            'failed': stats['failed'],
            'delayed': stats['delayed'],
            'success_rate': round(success_rate, 1),
            'percentages': {
                'delivered': round((stats['delivered'] / total * 100), 1) if total > 0 else 0,
                'failed': round((stats['failed'] / total * 100), 1) if total > 0 else 0,
                'delayed': round((stats['delayed'] / total * 100), 1) if total > 0 else 0
            }
        }

    @staticmethod
    def _get_top_drivers(period_months, limit=5):
        start_date = timezone.now() - timedelta(days=30 * period_months)
        top_drivers = Chauffeur.objects.filter(tournee__date_tournee__gte=start_date).annotate(
            total_tours=Count('tournee'),
            completed_tours=Count('tournee', filter=Q(tournee__statut='terminé') if hasattr(Tournee, 'statut') else Q())
        ).order_by('-total_tours')[:limit]
        
        drivers_list = []
        for driver in top_drivers:
            total = driver.total_tours
            rate = (driver.completed_tours / total * 100) if total > 0 else 0
            drivers_list.append({
                'name': f"{driver.prenom} {driver.nom}",
                'badge': getattr(driver, 'matricule', f"CH{driver.id:03d}"),
                'total_tours': total,
                'completed_tours': driver.completed_tours,
                'completion_rate': round(rate, 1)
            })
        return drivers_list

    @staticmethod
    def _get_incident_zones(period_months=12, limit=10):
        start_date = timezone.now() - timedelta(days=30 * period_months)
        incident_zones = Incident.objects.filter(date_reported__gte=start_date).values('tour__expeditions__numBureau__ville').annotate(count=Count('id')).order_by('-count')[:limit]
        return {
            'labels': [zone['tour__expeditions__numBureau__ville'] or "Zone Inconnue" for zone in incident_zones],
            'data': [zone['count'] for zone in incident_zones]
        }

    @staticmethod
    def _get_peak_activity_months(period_months):
        start_date = timezone.now() - timedelta(days=30 * period_months)
        monthly_tours = Tournee.objects.filter(date_tournee__gte=start_date).annotate(month=TruncMonth('date_tournee')).values('month').annotate(count=Count('id')).order_by('month')
        month_names_fr = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
        counts_dict = {entry['month'].strftime('%b'): entry['count'] for entry in monthly_tours}
        counts = [counts_dict.get(month, 0) for month in month_names_fr]
        return {'labels': month_names_fr, 'counts': counts, 'max_value': max(counts) if counts else 0}

    @staticmethod
    def _get_tours_per_month_chart(period_months):
        peak_data = DashboardCalculator._get_peak_activity_months(period_months)
        max_val = peak_data['max_value']
        scaled_data = [(count / max_val * 100) if max_val > 0 else 0 for count in peak_data['counts']]
        return {'labels': peak_data['labels'], 'data': [round(v, 1) for v in scaled_data], 'actual_counts': peak_data['counts'], 'max_scale': 100}