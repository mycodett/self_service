import pandas as pd
from django.utils.dateparse import parse_date, parse_datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ExcelUploadForm, NotificationForm, FeedbackForm
from .models import ExcelData, Notification, UserQuery, Feedback
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.http import HttpResponseForbidden

def admin_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to access this page.")
        return function(request, *args, **kwargs)
    
    return wrap

def user_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_staff:
            return HttpResponseForbidden("This page is for regular users only.")
        return function(request, *args, **kwargs)
    
    return wrap

# Custom Login View
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('upload_excel')  # Admin page
            else:
                return redirect('user_dashboard')  # User dashboard
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')  # Login page

# Custom Logout View
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout

# Admin Upload Excel View
@login_required
@admin_required
def upload_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']

        # Clear existing data
        ExcelData.objects.all().delete()

        try:
            # Read uploaded Excel file
            df = pd.read_excel(excel_file)

            # Replace NaN with None
            df = df.where(pd.notna(df), None)

            # Prepare data for insertion
            upload_timestamp = timezone.localtime(timezone.now())
            excel_data_list = []

            for index, row in df.iterrows():
                row = row.fillna('')  # Replace NaN with empty strings

                # Parse dates if they exist
                uploaded_on = parse_datetime(str(row['Uploaded on'])) if row['Uploaded on'] else None
                allocated_on = parse_datetime(str(row['Allocated on'])) if row['Allocated on'] else None
                from_date = parse_datetime(str(row['From Date'])) if row['From Date'] else None

                # Create ExcelData objects
                excel_data = ExcelData(
                    process_id=row['Process id'],
                    cg_pno=row['CG_PNO'],
                    name=row['Name'],
                    rank=row['RANK'],
                    unit_descriptions=row['Unit Descriptions'],
                    batch=row['Batch'],
                    uploaded_on=uploaded_on,
                    user_name=row['User Name'],
                    process_name=row['Process Name'],
                    form_no=row['Form no.'],
                    refrence_type=row['Refrence Type'],
                    form_type=row['Form Type Descriptio'],
                    from_date=from_date,
                    allocated_on=allocated_on,
                    task_to=row['Task to'],
                    status=row['STATUS'],
                    stage=row['STAGE'],
                    approver_remarks=row['APPROVER REMARKS'],
                    verifier_remarks=row['VERIFIER REMARKS'],
                    initiator_remarks=row['INITIATOR REMARKS'],
                    upload_date=upload_timestamp
                )

                excel_data_list.append(excel_data)

                # Commit every 500 rows
                if len(excel_data_list) >= 500:
                    with transaction.atomic():
                        ExcelData.objects.bulk_create(excel_data_list)
                    excel_data_list.clear()

            # Insert remaining rows
            if excel_data_list:
                with transaction.atomic():
                    ExcelData.objects.bulk_create(excel_data_list)

            messages.success(request, "Data uploaded successfully.")
            return redirect('upload_excel')

        except Exception as e:
            messages.error(request, f"Error processing the file: {e}")
            return redirect('upload_excel')

    form = ExcelUploadForm()
    return render(request, 'a_upload.html', {'form': form})

# Admin Notifications View
@login_required
@admin_required
def admin_notifications(request):
    notification_id = request.GET.get('edit')
    notification = None

    # Editing an Existing Notification
    if notification_id:
        notification = get_object_or_404(Notification, id=notification_id)
        if request.method == "POST":
            form = NotificationForm(request.POST, instance=notification)
            if form.is_valid():
                form.save()
                return redirect('admin-notifications')
        else:
            form = NotificationForm(instance=notification)
    else:
        # Adding a New Notification
        if request.method == "POST":
            form = NotificationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('admin-notifications')
        else:
            form = NotificationForm()

    notifications = Notification.objects.all()
    if 'delete' in request.GET:
        notification_id = request.GET['delete']
        notification = get_object_or_404(Notification, id=notification_id)
        notification.delete()
        return redirect('admin-notifications')

    return render(request, 'a_notifications.html', {'form': form, 'notifications': notifications, 'editing': notification})

# User Dashboard View
@login_required
@user_required
def user_dashboard(request):
    return render(request, 'u_dashboard.html')

# User Query Submission
@login_required
@user_required
def user_new_query(request):
    if request.method == 'POST':
        query_text = request.POST['query_text']
        query = UserQuery(user=request.user, query_text=query_text)
        query.save()
        messages.success(request, "Your query has been submitted successfully.")
        return redirect('user_dashboard')
    return render(request, 'user_new_query.html')

# User Queries View
@login_required
@user_required
def user_my_query(request):
    queries = UserQuery.objects.filter(user=request.user)
    return render(request, 'user_my_query.html', {'queries': queries})

# Admin Query Handling
@login_required
@admin_required
def admin_new_query(request):
    queries = UserQuery.objects.all()
    return render(request, 'a_reply_query.html', {'queries': queries})

# Admin Reply to User Query
@login_required
@admin_required
def admin_reply_to_query(request, query_id):
    query = get_object_or_404(UserQuery, id=query_id)
    if request.method == 'POST':
        reply = request.POST['reply']
        query.reply = reply
        query.save()
        messages.success(request, "Query has been replied.")
        return redirect('admin_new_query')
    return render(request, 'admin_old_query.html', {'query': query})

# Admin Feedback View
@login_required
@admin_required
def admin_feedback(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'admin_feedback.html', {'feedbacks': feedbacks})

# User Feedback View
@login_required
@user_required
def user_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your feedback.")
            return redirect('user_dashboard')
    else:
        form = FeedbackForm()
    return render(request, 'user_feedback.html', {'form': form})

# User Logout View (Redirects to login)
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@admin_required
def admin_notifications(request):
    notification_id = request.GET.get('edit')  # Check if there's an 'edit' parameter in the URL
    notification = None
    
    # Handle Editing an Existing Notification
    if notification_id:
        notification = get_object_or_404(Notification, id=notification_id)
        if request.method == "POST":
            form = NotificationForm(request.POST, instance=notification)
            if form.is_valid():
                form.save()
                return redirect('admin-notifications')  # Redirect to the same page after saving
        else:
            form = NotificationForm(instance=notification)
    else:
        # Handle Adding a New Notification
        if request.method == "POST":
            form = NotificationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('admin-notifications')  # Redirect to the same page after saving
        else:
            form = NotificationForm()

    # Handle Deleting Notifications
    notifications = Notification.objects.all()
    if 'delete' in request.GET:
        notification_id = request.GET['delete']
        notification = get_object_or_404(Notification, id=notification_id)
        notification.delete()
        return redirect('admin-notifications')

    return render(request, 'a_notifications.html', {'form': form, 'notifications': notifications, 'editing': notification})




# # User Page to View All Notifications
@login_required
@user_required
def user_notifications(request):
    notifications = Notification.objects.all()
    return render(request, 'u_notifications.html', {'notifications': notifications})

@login_required
@admin_required
def admin_about(request):
    return render(request, "a_about.html")

# # def admin_feedback(request):
# #     return render(request, "a_feedback.html")

# #User views
# @login_required
# @user_required
# def user_dashboard(request):
#     return render(request, 'u_dashboard.html')

# # def user_notifications(request):
# #     return render(request, "u_notifications.html")

@login_required
@user_required
def user_pf_status(request):
    results = []
    query_params = {}

    # Capture the search inputs from the GET request
    cg_pno = request.GET.get('cg_pno', '').strip()
    unit_descriptions = request.GET.get('unit_descriptions', '').strip()
    form_no = request.GET.get('form_no', '').strip()
    form_type = request.GET.get('form_type', '').strip()

    # Build the filter dictionary only for non-empty values
    if cg_pno:
        query_params['cg_pno__icontains'] = cg_pno
    if unit_descriptions:
        query_params['unit_descriptions__icontains'] = unit_descriptions
    if form_no:
        query_params['form_no__icontains'] = form_no
    if form_type:
        query_params['form_type__icontains'] = form_type

    # If there is any parameter to filter, perform the query
    if query_params:
        results = ExcelData.objects.filter(**query_params)

    return render(request, 'u_pf.html', {'results': results})


@login_required
@user_required
def user_about(request):
    return render(request, "u_about.html")


@login_required
@user_required
def user_new_query(request):
    if request.method == 'POST':
        pf_no = request.POST['pf_no']
        pf_unit = request.POST['pf_unit']
        description = request.POST['description']
        query = UserQuery(user=request.user, pf_no=pf_no, pf_unit=pf_unit, description=description)
        query.save()
        messages.success(request, "Your query has been submitted successfully.")
        return redirect('user_dashboard')
    return render(request, 'u_submit_query.html')


@login_required
@user_required
def user_my_query(request):
    queries = UserQuery.objects.filter(user=request.user)  # Only get queries for the logged-in user
    return render(request, 'u_my_query.html', {'queries': queries})



@login_required
@admin_required
def admin_new_query(request):
    all_queries = UserQuery.objects.filter(admin_reply__isnull=True)  # Only show queries without replies
    
    if request.method == 'POST':
        query_id = request.POST.get('query_id')  # Get the query ID from the form
        reply = request.POST.get('admin_reply')  # Get the reply text

        # Get the query by ID and update it with the admin's reply
        query = get_object_or_404(UserQuery, id=query_id)
        query.admin_reply = reply
        query.save()  # Save the reply to the query
        
        messages.success(request, "Query has been replied to successfully.")
        return redirect('admin_new_query')  # Redirect to the 'admin_old_query' after replying to the query
    
    return render(request, 'a_reply_query.html', {'all_queries': all_queries})

@login_required
@admin_required
def admin_old_query(request):
    # Only show queries that have an admin reply
    all_queries = UserQuery.objects.filter(admin_reply__isnull=False)
    return render(request, 'a_old_query.html', {'all_queries': all_queries})


@login_required
@user_required
def user_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)  # Create instance without saving
            feedback.user = request.user        # Assign the logged-in user
            feedback.save()                    # Save with user set
            messages.success(request, 'Thank you for your feedback! It has been successfully submitted.')
    else:
        form = FeedbackForm()

    return render(request, 'u_feedback.html', {'form': form})

# View for Admin to See All Feedbacks (without login required)
@login_required
@admin_required
def admin_feedback(request):
    # Optionally add a success message for admins
    messages.success(request, 'Here are the feedbacks submitted by users.')

    # Retrieve all feedbacks from the database
    feedbacks = Feedback.objects.all()
    
    return render(request, 'a_feedback.html', {'feedbacks': feedbacks})
