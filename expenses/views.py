from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Sum
from django.utils import timezone
from .models import Budget, Expense
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Budget
from .forms import BudgetForm
from django.utils import timezone
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Budget
from .forms import BudgetForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Expense
from django.utils.timezone import now
from django.shortcuts import render
import calendar


@login_required
def dashboard(request):
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    expenses = Expense.objects.filter(user=request.user, date__month=current_month, date__year=current_year)
    total = sum(exp.amount for exp in expenses)

    try:
        budget = Budget.objects.get(user=request.user, month=current_month, year=current_year)
    except Budget.DoesNotExist:
        budget = None

    greeting = get_greeting()
    quote = get_random_quote()

    context = {
        'expenses': expenses,
        'total': total,
        'budget': budget,
        'greeting': greeting,
        'quote': quote,
    }
    return render(request, 'expenses/dashboard.html', context)

# add_expense
@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})


# edit_budget
@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully.')
            return redirect('dashboard')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/edit_expense.html', {'form': form})

# delete_expense

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully.')
        return redirect('dashboard')
    return render(request, 'expenses/delete_expense.html', {'expense': expense})


# set_budget
@login_required
def set_budget(request):
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    # Try to get existing budget for current month and user
    budget = Budget.objects.filter(user=request.user, month=current_month, year=current_year).first()

    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)  # instance=budget to update if exists
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.month = current_month
            budget.year = current_year
            budget.save()
            return redirect('dashboard')  # Redirect after successful save
    else:
        form = BudgetForm(instance=budget)

    return render(request, 'expenses/set_budget.html', {'form': form})


import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt

import calendar
import io
import base64
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Expense

@login_required
def monthly_history(request):
    user = request.user
    today = timezone.now()
    current_year = today.year
    current_month = today.month

    expenses = Expense.objects.filter(
        user=user,
        date__year=current_year,
        date__month__lte=current_month
    )

    summary = {}
    for expense in expenses:
        key = (expense.date.year, expense.date.month)
        summary.setdefault(key, 0)
        summary[key] += float(expense.amount)

    sorted_summary = sorted(summary.items())
    formatted_summary = [
        {"month": calendar.month_name[month], "year": year, "amount": amount}
        for (year, month), amount in sorted_summary
    ]

    # Prepare data for chart
    months = [f"{entry['month']}" for entry in formatted_summary]
    amounts = [entry['amount'] for entry in formatted_summary]

    # Plot line chart with filled area
    plt.figure(figsize=(10, 4))
    plt.plot(months, amounts, marker='o', color='#FF6F61', linewidth=2)
    plt.fill_between(months, amounts, color='#FFB6B9', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Total Expenses (BDT)")
    plt.title("Monthly Expenses Comparison")
    plt.tight_layout()

    # Save chart as base64 image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_base64 = base64.b64encode(buf.getvalue()).decode()
    plt.close()

    return render(request, 'expenses/monthly_history.html', {
        'summary': formatted_summary,
        'chart_base64': chart_base64
    })




# edit_budget
@login_required
def edit_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget updated successfully.')
            return redirect('dashboard')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'expenses/edit_budget.html', {'form': form})



# get_greeting
def get_greeting():
    current_hour = timezone.now().hour
    if 5 <= current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 17:
        return "Good afternoon"
    elif 17 <= current_hour < 21:
        return "Good evening"
    else:
        return "Hello"

import random

QUOTES = [
    "Life is what happens when you're busy making other plans. — John Lennon",
    "The purpose of our lives is to be happy. — Dalai Lama",
    "Keep your face always toward the sunshine—and shadows will fall behind you. — Walt Whitman",
    "Believe you can and you're halfway there. — Theodore Roosevelt",
    "In the middle of every difficulty lies opportunity. — Albert Einstein",
]

def get_random_quote():
    return random.choice(QUOTES)
