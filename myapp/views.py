from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from django.db.models import Sum
import datetime

# Create your views here.


def index(request):

    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()

    expense_form = ExpenseForm()
    expenses = Expense.objects.all()

    # Total Spend
    total_expense = expenses.aggregate(Sum('price'))
    '''
    aggregate : such as calculating the sum, average, minimum, maximum, etc., 
    of a specific field across the queryset. It returns a dictionary containing 
    the aggregated results. 
    '''

    # Expense of today
    today = datetime.date.today()

    # SUM of Yearly Expense (365 dyas)
    last_year = today - datetime.timedelta(days=365)
    yearly_data = Expense.objects.filter(date__gt=last_year)
    yearly_sum = yearly_data.aggregate(Sum('price'))

    # SUM of Monthly Expense (30 days)
    last_month = today - datetime.timedelta(days=30)
    monthly_data = Expense.objects.filter(date__gt=last_month)
    monthly_sum = monthly_data.aggregate(Sum('price'))

    # SUM of Weekly Expense (7 days)
    last_week = today - datetime.timedelta(days=7)
    weekly_data = Expense.objects.filter(date__gt=last_week)
    weekly_sum = weekly_data.aggregate(Sum('price'))

    # Past 30 days expenses
    daily_sums = Expense.objects.filter(date__gte=last_month).values(
        'date').order_by('date').annotate(sum=Sum('price'))

    # Category expenses
    categorical_sums = Expense.objects.filter().values(
        'category').order_by('category').annotate(sum=Sum('price'))

    '''
    *annotate :  annotate is used to add computed fields to each object in the queryset based on aggregate functions
    '''
    return render(request, 'myapp/index.html', {'expenses': expenses, 'expense_form': expense_form, 'total_expense': total_expense,
                                                'yearly_sum': yearly_sum, 'monthly_sum': monthly_sum, 'weekly_sum': weekly_sum, 'daily_sums': daily_sums, 'categorical_sums': categorical_sums})


def edit(request, id):
    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)

    if request.method == "POST":
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'myapp/edit.html', {'exepnse': expense, 'expense_form': expense_form})


def delete(request, id):

    if request.method == "POST" and 'delete' in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')
