from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .RAG import generate_rag_response

from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

from income.models import Income
from expense.models import Expense


# Function to get user's data
def get_user_financial_summary(user):
    today = timezone.now().date()
    three_months_ago = today - timedelta(days=90)

    incomes = (
        Income.objects.filter(user=user, date__gte=three_months_ago)
        .values("date__year", "date__month", "category")
        .annotate(total=Sum("amount"))
        .order_by("date__year", "date__month")
    )

    expenses = (
        Expense.objects.filter(user=user, date__gte=three_months_ago)
        .values("date__year", "date__month", "category")
        .annotate(total=Sum("amount"))
        .order_by("date__year", "date__month")
    )

    return {
        "incomes": list(incomes),
        "expenses": list(expenses),
    }


class financialInsightsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_data = get_user_financial_summary(user)

        # Generate RAG response
        try:
            response = generate_rag_response(user_data)
            return Response({"insights": response})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
