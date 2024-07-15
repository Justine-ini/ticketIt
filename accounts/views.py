from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import AddcompanyForm, CreateUserForm, TicketForm, UserProfileForm
from .models import Company, Sector, Ticket, UserProfile
from django.contrib.auth.models import User

from django.core.mail import send_mail
import smtplib


def loginPage(request):
  if request.method == 'POST':
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect("dashboard")

  return render(request, "accounts/login.html")

def register(request):
  form = CreateUserForm()
  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
    #   
    #   email = form.cleaned_data['email']
    #   password = form.cleaned_data['password']
    #   user = User.objects.create_user( username=username, email=email, password=password)
    #   user.save()
        username = form.cleaned_data.get('username')
        form.save()
        messages.success(request, username +' your account has been successfully created!' )
        return redirect('login')
#       return redirect('login')
#     else:
#         print('invalid form')
#         print(form.errors)
#   else:
#     form = CreateUserForm()
  context = {
    'form': form,
  }

  return render(request, "accounts/register.html", context)

def add_company(request):
  if request.method == 'POST':
    form = AddcompanyForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Company added Successfully!")
        return redirect('dashboard')
  else:
      form = AddcompanyForm()
  context ={
      "form":form
   }
  return render(request, "accounts/add_company.html", context)    


def create_ticket(request):
  print("checking request type")
  if request.method == 'POST':
      print("request method is post")
      # Create a form instance with the POST data
      form = TicketForm(request.POST)
      
      # Check if the form is valid
      if form.is_valid():
          print("form is valid")
          
          # Create a Ticket instance without saving to the database yet
          ticket = form.save(commit=False)
          
          # Set the user_email field value explicitly
          ticket.user_email = request.user.email
          
          # Save the Ticket instance to the database
          ticket.save()
          print("form is saved")
          
          # Display a success message to the user
          messages.success(request, "Your Form is Submitted Successfully!")
          
          # Redirect the user to the 'ticket_list' page
          return redirect('dashboard')
  else:
      # Create a form instance with the initial user_email value
      form = TicketForm(initial={'user_email': request.user.email})
      print("form is either not valid or saved")
  
  # Render the form in the 'accounts/dashboard.html' template
  return render(request, 'accounts/dashboard.html', {'form': form})


def ticket_edit(request, pk):
  ticket = get_object_or_404(Ticket, pk=pk)
  form = TicketForm(instance=ticket)
  print("checking request type")
  if request.method == 'POST':
      print("request method is post")
      # Create a form instance with the POST data
      form = TicketForm(request.POST, instance=ticket)
      
      # Check if the form is valid
      if form.is_valid():
          print("form is valid")
          
          # Create a Ticket instance without saving to the database yet
          ticket = form.save(commit=False)
          
          # Set the user_email field value explicitly
          ticket.user_email = request.user.email
          
          # Save the Ticket instance to the database
          form.save()
          print("form is saved")
          
          # Display a success message to the user
          messages.success(request, "Your Form is Updated Successfully!")
          
          # Redirect the user to the 'ticket_list' page
          return redirect('dashboard')
          # return redirect('ticket_list')
  else:
      # Create a form instance with the initial user_email value
      form = TicketForm(initial={'user_email': request.user.email}, instance=ticket)
      print("form is either not valid or saved")
  
  # Render the form in the 'accounts/dashboard.html' template
  return render(request, 'accounts/ticket_edit.html', {'form': form})


# All Tickets
def ticket_detail(request, pk):
  tickets = get_object_or_404(Ticket, pk=pk)
  return render(request, 'accounts/ticket_detail.html', {'tickets': tickets})


def dashboard(request):
    # Retrieve the current user
    user = request.user

    # Retrieve all sectors and tickets
    sectors = Sector.objects.all()
    tickets = Ticket.objects.all()

    # Calculate the total, resolved, and pending complaints
    total_complaint = tickets.count()
    resolved_complaint = tickets.filter(status=True).count()
    pending_complaint = tickets.filter(status=False).count()

    # Initialize the context dictionary
    context = {
        "user": user,
        "ticket": tickets,
        "total_complaint": total_complaint,
        "resolved_complaint": resolved_complaint,
        "pending_complaint": pending_complaint,
        "sector": sectors,
    }

    if request.method == 'POST':
        # Handle form submission
        form = TicketForm(request.POST)
        if form.is_valid():
            # Save the form but do not commit to the database yet
            ticket = form.save(commit=False)
            # Set the user_email field explicitly
            ticket.user_email = request.user.email
            # Save the ticket instance to the database
            ticket.save()
            # Display success message
            messages.success(request, "Your Form is Submitted Successfully!")
            # Redirect to the dashboard
            return redirect('dashboard')
    else:
        # Initialize the form with the user's email
        form = TicketForm(initial={'user_email': request.user.email})

    # Add the form to the context
    context['form'] = form

    # Render the dashboard template with the context
    return render(request, 'accounts/dashboard.html', context)

def view_profile(request, username):
  user = get_object_or_404(User, username=username)
  profile = get_object_or_404(UserProfile, user=user)
  return render(request, 'accounts/view_profile.html', {'user': user, 'profile': profile})


def logoutView(request):
  logout(request)
  messages.info(request, "You are logged out")
  return redirect("login")

def ticket(request, pk):
  ticket = get_object_or_404(Ticket, pk=pk)

  context = {
    "ticket": ticket
  }
  return render(request, "accounts/dashboard.html", context)


def update_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'update_ticket.html', {'form': form})
     

# @login_required
def ticket_list(request):
  
  user = request.user
  sector = Sector.objects.all()
  ticket = Ticket.objects.all()
  total_complaint = ticket.count()
  resolved_complaint = ticket.filter(status=True).count()  # Assuming 'status=True' means resolved
  pending_complaint = ticket.filter(status=False).count()  # Assuming 'status=False' means pending
  context = { 
    "user":user,
    "ticket": ticket,
    "total_complaint": total_complaint,
    "resolved_complaint": resolved_complaint,
    "pending_complaint": pending_complaint,
    "sector": sector,
    }
  return render(request, 'accounts/ticket_list.html', context)


# @login_required
def ticket_delete(request, pk):
  ticket = get_object_or_404(Ticket, pk=pk)
  if request.method == 'POST':
      ticket.delete()
      return redirect('dashboard')

  return render(request, 'accounts/dashboard.html', {'ticket': ticket})




