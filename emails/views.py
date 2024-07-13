from django.shortcuts import render, get_object_or_404, redirect
from .models import EmailData
from .forms import EmailDataForm


def email_list(request):
    emails = EmailData.objects.all()
    return render(request, 'emails/email_list.html', {'emails': emails})


def email_detail(request, pk):
    email = get_object_or_404(EmailData, pk=pk)
    return render(request, 'emails/email_detail.html', {'email': email})


def email_create(request):
    if request.method == 'POST':
        form = EmailDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('email_list')
    else:
        form = EmailDataForm()
    return render(request, 'emails/email_form.html', {'form': form})


def email_update(request, pk):
    email = get_object_or_404(EmailData, pk=pk)
    if request.method == 'POST':
        form = EmailDataForm(request.POST, instance=email)
        if form.is_valid():
            form.save()
            return redirect('email_list')
    else:
        form = EmailDataForm(instance=email)
    return render(request, 'emails/email_form.html', {'form': form})


def email_delete(request, pk):
    email = get_object_or_404(EmailData, pk=pk)
    if request.method == 'POST':
        email.delete()
        return redirect('email_list')
    return render(request, 'emails/email_confirm_delete.html', {'email': email})
