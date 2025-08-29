from .models import Income
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import IncomeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from django.db.models import Sum

# Functions to aggregate income data


def aggregate_by_current_month(user):
    now = datetime.now()
    return (
        Income.objects.filter(
            user=user,
            date__year=now.year,
            date__month=now.month
        ).aggregate(total=Sum('amount'))['total'] or 0
    )


def aggregate_by_category(user):
    return (
        Income.objects.filter(user=user)
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )


class IncomeListCreateView(ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Income.objects.all()
        params = self.request.query_params

        date = params.get('date')
        category = params.get('category')
        start_date = params.get("start_date")
        end_date = params.get("end_date")

        if category:
            queryset = queryset.filter(category=category)
        if date:
            queryset = queryset.filter(date=date)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        return queryset


class IncomeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]


class DashboardView(APIView):
    def get(self, request):
        user = request.user
        month_total = aggregate_by_current_month(user)
        category_totals = aggregate_by_category(user)

        return Response({
            "month_total": month_total,
            "category_totals": category_totals
        })

    from datetime import datetime
