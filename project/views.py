from django.shortcuts import render,redirect
from .models import Appointment,status_point,Preference,Building,assign_point_and_preference,senior_staff_appointment,designation_point,Preference_senior_staff,junior_staff_appointment,designation_point_junior,Preference_junior_staff,assign_point_and_preference_senior,assign_point_and_preference_junior
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from datetime import datetime, timedelta

def admin_manage_buildings(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        vacant_rooms = request.POST.get('vacant_rooms')
        rent_charge = request.POST.get('rent')
        building_location = request.POST.get('Location')

        if name and category and vacant_rooms:
            Building.objects.create(
                name=name,
                category=category,
                rent_charge=rent_charge,
                location=building_location,
                vacant_rooms=int(vacant_rooms)
            )
            messages.add_message(request, messages.SUCCESS, 'Building added successfully', extra_tags='building_added')
            return redirect('manage_buildings')
        else:
            messages.error(request, 'Please provide all required fields')

    buildings = Building.objects.all()
    return render(request, 'admin_manage.html', {'buildings': buildings})


def view_all_users(request):
    applications = Appointment.objects.all()
    senior_staff = senior_staff_appointment.objects.all()
    junior_staff = junior_staff_appointment.objects.all()
    
    # Fetch preferences for each category
    preferences = Preference.objects.select_related('application').all()
    senior_preferences = Preference_senior_staff.objects.select_related('application').all()  
    junior_preferences = Preference_junior_staff.objects.select_related('application').all()

    # Create a dictionary to group preferences by staff number for each category
    preferences_dict = {}
    senior_preferences_dict = {}
    junior_preferences_dict = {}

    # Populate preferences_dict for applications
    for app in applications:
        staff_number = app.staff_number
        preferences_dict[staff_number] = {
            'name': app.name,
            'department': app.department,
            'mobile_Number': app.mobile_no,
            'dateOf_Uni_Appointment': app.dateOf_Uni_Appointment,
            'presentUni_bungalow': app.presentUni_bungalow,
            'date_of_occupation_ofAccomodation': app.date_of_occupation_ofAccomodation,
            'studyLeave_from': app.studyLeave_from,
            'studyLeave_to': app.studyLeave_to,
            'marital_status': app.marital_status,
            'spouse_id': app.spouse_id,
            'duty_status': app.duty_status,
            'duty_status_type': app.duty_status_type,
            'num_of_children': app.num_of_children,
            'date_of_duty': app.date_of_duty,
            'present_accommodation': app.present_accommodation,
            'preferences': []
        }

    # Add preferences to the applications' dictionary
    for pref in preferences:
        staff_number = pref.application.staff_number
        if staff_number in preferences_dict:
            preferences_dict[staff_number]['preferences'].append(pref.preference)
    
    # Populate senior_preferences_dict for senior staff details
    for staff in senior_staff:
        staff_number = staff.staff_number
        senior_preferences_dict[staff_number] = {
            'name': staff.name,
            'department': staff.department,
            'mobile_Number': staff.mobile_no,
            'dateOf_Uni_Appointment': staff.dateOf_Uni_Appointment,
            'presentUni_bungalow': staff.presentUni_bungalow,
            'date_of_occupation_ofAccomodation': staff.date_of_occupation_ofAccomodation,
            'marital_status': staff.marital_status,
            'num_of_children': staff.num_of_children,
            'total_points': staff.total_points,
            'present_accommodation': staff.present_accommodation,
            'preferences': []
        }

    # Add preferences to the senior staff's dictionary
    for pref in senior_preferences:
        staff_number = pref.application.staff_number
        if staff_number in senior_preferences_dict:
            senior_preferences_dict[staff_number]['preferences'].append(pref.preference)
    
    # Populate junior_preferences_dict for junior staff details
    for staff in junior_staff:
        staff_number = staff.staff_number
        junior_preferences_dict[staff_number] = {
            'name': staff.name,
            'department': staff.department,
            'mobile_Number': staff.mobile_no,
            'dateOf_Uni_Appointment': staff.dateOf_Uni_Appointment,
            'presentUni_bungalow': staff.presentUni_bungalow,
            'marital_status': staff.marital_status,
            'num_of_children': staff.num_of_children,
            'total_points': staff.total_points,
            'preferences': []
        }

    # Add preferences to the junior staff's dictionary
    for pref in junior_preferences:
        staff_number = pref.application.staff_number
        if staff_number in junior_preferences_dict:
            junior_preferences_dict[staff_number]['preferences'].append(pref.preference)

    return render(request, 'all_users.html', {
        'applications': applications,
        'senior_staff': senior_staff,
        'junior_staff': junior_staff,
        'preferences_dict': preferences_dict,
        'senior_preferences_dict': senior_preferences_dict,
        'junior_preferences_dict': junior_preferences_dict
    })


def calculate_accommodation_points(present_accommodation, present_accommodation_date):
    if present_accommodation is None or present_accommodation_date is None:
        return 0  # Skip calculation if either value is None

    present_date = datetime.strptime(present_accommodation_date, '%Y-%m-%d')
    current_date = datetime.now()
    months_of_stay = (current_date.year - present_date.year) * 12 + abs(current_date.month - present_date.month) + 1

    if present_accommodation == 'off_campus':
        return months_of_stay // 3
    elif present_accommodation == 'on_campus':
        return months_of_stay // 6
    elif present_accommodation == 'temporary_accommodation':
        return months_of_stay // 2
    elif present_accommodation == 'not_accommodated':
        return months_of_stay
    else:
        return 0



def cal_marital_points(duty_status, marital_status, num_of_children, date_of_duty=None):
    try:
        total_point = 0
        if date_of_duty:
            months_ = datetime.now()
            duty = datetime.strptime(date_of_duty, '%Y-%m-%d')
            months_of_duty = ((months_.year - duty.year) * 12) + (months_.month - duty.month)
        else:
            months_of_duty = 0  # Set to 0 if date_of_duty is None
        
        if marital_status == 'married':
            total_point += 2
        
        if num_of_children:
                total_for_children = num_of_children * 1
                if total_for_children<=5:
                    total_point+=total_for_children
                else:
                    total_point+=5

        if duty_status:
            if months_of_duty >= 12:
                total_point += 3
        print(duty_status)
        return total_point

    except ValueError as e:
        print(e)
        raise ValueError('Invalid date format. Please use YYYY-MM-DD.')

def calculate_status_points(initial_point, dateOf_Uni_Appointment, study_leaveFrom=None, study_leaveTo=None):
    try:
        total_points = 0

        # Calculate points based on months in service
        appointment_date = datetime.strptime(dateOf_Uni_Appointment, '%Y-%m-%d')
        current_date = datetime.now()
        months_in_service = (current_date.year - appointment_date.year) * 12 + abs(current_date.month - appointment_date.month)
        print(f"month in service: {months_in_service}")
        # Remove months during the study leave from the service period calculation
        if study_leaveFrom and study_leaveTo:
            leave_from = datetime.strptime(study_leaveFrom, '%Y-%m-%d')
            leave_to = datetime.strptime(study_leaveTo, '%Y-%m-%d')
            leave_months = (leave_to.year - leave_from.year) * 12 + abs(leave_to.month - leave_from.month) + 1
            months_in_service -= leave_months
            print(f"leave: {leave_months}")
            print(f"month after leave: {months_in_service}")
        
        # Assign 1 point for each month in service
        total_points += months_in_service

        # Calculate study leave points
        if study_leaveFrom and study_leaveTo:
            leave_from = datetime.strptime(study_leaveFrom, '%Y-%m-%d')
            leave_to = datetime.strptime(study_leaveTo, '%Y-%m-%d')
            current_month = leave_from
            
            while current_month <= leave_to:
                consecutive_leave_months = 1
                next_month = current_month + timedelta(days=32)
                next_month = next_month.replace(day=1)

                while next_month <= leave_to:
                    consecutive_leave_months += 1
                    next_month += timedelta(days=32)
                    next_month = next_month.replace(day=1)

                if consecutive_leave_months >= 3:
                    total_points += 1
                
                current_month = next_month
            else:
                total_points+=1
                current_month += timedelta(days=32)

        return total_points + initial_point
    
    except ValueError:
        raise ValueError('Invalid date format. Please use YYYY-MM-DD.')
def delete_building(request, building_id):
    if request.method == 'POST':
        building = get_object_or_404(Building, id=building_id)
        building.delete()
        return redirect(reverse('manage_buildings'))
    return redirect(reverse('manage_buildings'))


def update_building(request, building_id):
    if request.method == 'POST':
        building = get_object_or_404(Building, id=building_id)
        
        # Extract data from POST request
        name = request.POST.get('name')
        category = request.POST.get('category')
        rent_charge = request.POST.get('rent')
        location = request.POST.get('Location')
        vacant_rooms = request.POST.get('vacant_rooms')
        
        # Update the building instance
        if name and category and rent_charge and location and vacant_rooms:
            building.name = name
            building.category = category
            building.rent_charge = rent_charge
            building.location = location
            building.vacant_rooms = vacant_rooms
            building.save()
    
    return redirect(reverse('manage_buildings'))


def get_buildings(request):
    staff_number = request.GET.get('staff_number')
    category = ''

    # Determine the category based on the staff number prefix
    if staff_number.startswith('sm'):
        category = 'senior_member'
    elif staff_number.startswith('ss'):
        category = 'senior_staff'
    elif staff_number.startswith('js'):
        category = 'junior_staff'

    # Fetch buildings based on the determined category
    available_buildings = Building.objects.filter(category=category, vacant_rooms__gt=0)
    building_names = [building.name for building in available_buildings]

    # Return the building names as a JSON response
    return JsonResponse({'preferences': building_names})

def view_all_preferences(request):
    applications = Appointment.objects.all()
    preferences = Preference.objects.select_related('application').all()

    # Create a dictionary to group preferences by staff number
    preferences_dict = {}
    for pref in preferences:
        staff_number = pref.application.staff_number
        if staff_number not in preferences_dict:
            preferences_dict[staff_number] = {
                'name': pref.application.name,
                'department': pref.application.department,
                'preferences': []
            }
        preferences_dict[staff_number]['preferences'].append(pref.preference)
    
    return render(request, 'view_preferences.html', {
        'applications': applications,
        'preferences_dict': preferences_dict
    })


def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        staff_number = request.POST.get('staff_number')
        department = request.POST.get('department')
        mobile_number = request.POST.get('mobile_number')
        uni_appointment = request.POST.get('uni_appointment')
        bungalow_no = request.POST.get('bungalow_no', '')
        present_accommodation = request.POST.get('present_accomodation',None)
        present_accommodation_name = request.POST.get('present_accommodation_name')
        status_points = request.POST.get('status_point')
        study_leaveFrom = request.POST.get('study_leaveFrom', None)
        study_leaveTo = request.POST.get('study_leaveTo', None)
        marital_status = request.POST.get('marital_status', None)
        marital_input = request.POST.get('marriage_input', None)
        duty_status = request.POST.get('duty_status', None) == 'on'
        duty_status_type = request.POST.get('duty_status_type', None)
        num_of_children = request.POST.get('num_of_children', 0)
        date_of_duty = request.POST.get('date_of_duty', None)
        print(f"marriage : {marital_input}")

        try:
            status = status_point.objects.get(status_name=status_points)
        except status_point.DoesNotExist:
            messages.error(request, 'Status does not exist')
            return render(request, 'index.html')

        if Appointment.objects.filter(staff_number=staff_number).exists():
            messages.error(request, 'Staff number already used in application')
            return render(request, 'index.html')

        user = Appointment(
            name=name,
            staff_number=staff_number,
            department=department,
            mobile_no=mobile_number,
            dateOf_Uni_Appointment=uni_appointment,
            presentUni_bungalow=bungalow_no,
            initial_point=status.point,
            marital_status=marital_status,
            num_of_children=num_of_children,
        )
        if marital_status == "married" and marital_input:
            user.spouse_id = marital_input

        if study_leaveFrom:
            user.studyLeave_from = study_leaveFrom
        if study_leaveTo:
            user.studyLeave_to = study_leaveTo
        if date_of_duty:
            user.date_of_duty = date_of_duty
        if present_accommodation:
            user.date_of_occupation_ofAccomodation = present_accommodation
        if present_accommodation_name:
            user.present_accommodation = present_accommodation_name
        if duty_status:
            user.duty_status = duty_status
            user.duty_status_type = duty_status_type
        print(f"duty_status: {duty_status}")
        print(f"duty_status_type: {duty_status_type}")
        user.save() 
        staff_number = request.POST.get('staff_number')
        preference_count = int(request.POST.get('preference_count', 0))

        print(f"Staff Number: {staff_number}")
        print(f"Preference Count: {preference_count}")

        try:
            appointment = Appointment.objects.get(staff_number=staff_number)
        except Appointment.DoesNotExist:
            print("Appointment not found")
            return render(request, 'index.html', {'error': 'Appointment not found'})

        # Clear previous preferences for the same appointment
        Preference.objects.filter(application=appointment).delete()

        # Save preferences
        preferences_saved = 0
        for i in range(preference_count):
            preference_text = request.POST.get(f'preference_{i}')
            print(f"Preference {i}: {preference_text}")  # Debugging output
            if preference_text:
                Preference.objects.create(application=appointment, preference=preference_text)
                preferences_saved += 1
        
        print(f"Total Preferences Saved: {preferences_saved}")

        # Redirect or render success page
        return redirect('check_point')
    return render(request, 'index.html')



#senior staff appointment and calculation
#senior staff calculation functions
def calculate_service_points_seniorstaff(designation_point, dateOf_Uni_Appointment):
    try:
        total_points = 0

        # Calculate points based on months in service
        appointment_date = datetime.strptime(dateOf_Uni_Appointment, '%Y-%m-%d')
        current_date = datetime.now()
        years_in_service = int(((current_date.year - appointment_date.year) * 12 + abs(current_date.month - appointment_date.month)) / 12)
        
        # 2 points for each year of service
        total_points = years_in_service * 2

        

        return total_points + designation_point
    
    except ValueError:
        raise ValueError('Invalid date format. Please use YYYY-MM-DD.')


def calculate_present_accommodation_points_seniorstaff(present_accommodation, date_of_occupation_of_accommodation):
    try:
        if not present_accommodation or not date_of_occupation_of_accommodation:
            return 0  # Return 0 if any field is missing
        
        occupation_date = datetime.strptime(date_of_occupation_of_accommodation, '%Y-%m-%d')
        current_date = datetime.now()
        total_months_of_stay = (current_date.year - occupation_date.year) * 12 + abs(current_date.month - occupation_date.month) + 1

        if present_accommodation == 'Senior staff university accommodation':
            # 2 points for every 3 months of stay
            return (total_months_of_stay // 3) * 2
        elif present_accommodation == 'Junior Staff Accommodation' or present_accommodation == 'Not Accommodated':
            # 1 point for each month of stay
            return total_months_of_stay
        else:
            return 0  # No points for other types of accommodation

    except ValueError:
        raise ValueError('Invalid date format. Please use YYYY-MM-DD.')

def cal_marital_points_seniorstaff(marital_status, num_of_children):

    total_point = 0
        
    if marital_status == 'married':
        total_point += 2
        
    if num_of_children:
        total_for_children = num_of_children * 1
        if total_for_children<=5:
            total_point+=total_for_children
        else:
            total_point+=5
    return total_point


#senior staff appointment form
def senior_staff_app(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        staff_number = request.POST.get('staff_number')
        department = request.POST.get('department')
        mobile_number = request.POST.get('mobile_number')
        uni_appointment = request.POST.get('uni_appointment')
        bungalow_no = request.POST.get('bungalow_no', '')
        present_accommodation = request.POST.get('present_accomodation_date',None)
        designation_points = request.POST.get('status_point')
        marital_status = request.POST.get('marital_status', None)
        marital_input = request.POST.get('marriage_input', None)        
        num_of_children = request.POST.get('num_of_children', 0)
        present_accommodation_name = request.POST.get('present_accommodation_name')

        try:
            status = designation_point.objects.get(status_name=designation_points)
        except designation_point.DoesNotExist:
            messages.error(request, 'Status does not exist')
            return render(request, 'senior_staff_form.html')

        if senior_staff_appointment.objects.filter(staff_number=staff_number).exists():
            messages.error(request, 'Staff number already used in application')
            return render(request, 'senior_staff_form.html')
        user = senior_staff_appointment(
            name=name,
            staff_number=staff_number,
            department=department,
            mobile_no=mobile_number,
            dateOf_Uni_Appointment=uni_appointment,
            designation_point=status.point,
            marital_status=marital_status,
            num_of_children=num_of_children,
        )
        if marital_status == "married" and marital_input:
            user.spouse_id = marital_input
        if present_accommodation:
            user.date_of_occupation_ofAccomodation = present_accommodation
        if bungalow_no:
            user.presentUni_bungalow = bungalow_no
        if present_accommodation_name:
            user.present_accommodation = present_accommodation_name
        user.save() 
        staff_number = request.POST.get('staff_number')
        preference_count = int(request.POST.get('preference_count', 0))

        print(f"Staff Number: {staff_number}")
        print(f"Preference Count: {preference_count}")

        try:
            appointment = senior_staff_appointment.objects.get(staff_number=staff_number)
        except senior_staff_appointment.DoesNotExist:
            print("Appointment not found")
            return render(request, 'senior_staff_form.html', {'error': 'Appointment not found'})

        # Clear previous preferences for the same appointment
        Preference_senior_staff.objects.filter(application=appointment).delete()

        # Save preferences
        preferences_saved = 0
        for i in range(preference_count):
            preference_text = request.POST.get(f'preference_{i}')
            print(f"Preference {i}: {preference_text}")  # Debugging output
            if preference_text:
                Preference_senior_staff.objects.create(application=senior_staff_appointment, preference=preference_text)
                preferences_saved += 1
        
        print(f"Total Preferences Saved: {preferences_saved}")

        # Redirect or render success page
        return redirect('senior_staff_form')
    return render(request,'senior_staff_form.html')


#junior staff calculation functions
def calculate_service_points_juniorstaff(designation_point, dateOf_Uni_Appointment):
    try:
        total_points = 0

        # Calculate points based on months in service
        appointment_date = datetime.strptime(dateOf_Uni_Appointment, '%Y-%m-%d')
        current_date = datetime.now()
        years_in_service = int(((current_date.year - appointment_date.year) * 12 + abs(current_date.month - appointment_date.month)) / 12)
        print(f"years in service : {years_in_service}")
        # 2 points for each year of service
        total_points = years_in_service * 2

        return total_points + designation_point
    
    except ValueError:
        raise ValueError('Invalid date format. Please use YYYY-MM-DD.')



def cal_marital_points_juniorstaff(marital_status, num_of_children):

    total_point = 0
        
    if marital_status == 'married':
        total_point += 2
        
    if num_of_children:
        total_for_children = num_of_children * 1
        if total_for_children<=5:
            total_point+=total_for_children
        else:
            total_point+=5
    return total_point


#junior staff form application and checkpoint
def junior_staff(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        staff_number = request.POST.get('staff_number')
        department = request.POST.get('department')
        mobile_number = request.POST.get('mobile_number')
        uni_appointment = request.POST.get('uni_appointment')
        bungalow_no = request.POST.get('bungalow_no', '')
        designation_points = request.POST.get('status_point')
        marital_status = request.POST.get('marital_status', None)
        marital_input = request.POST.get('marriage_input', None)        
        num_of_children = request.POST.get('num_of_children', 0)

        try:
            status = designation_point_junior.objects.get(status_name=designation_points)
        except designation_point_junior.DoesNotExist:
            messages.error(request, 'Status does not exist')
            return render(request, 'junior_staff.html')

        if junior_staff_appointment.objects.filter(staff_number=staff_number).exists():
            messages.error(request, 'Staff number already used in application')
            return render(request, 'junior_staff.html')
        user = junior_staff_appointment(
            name=name,
            staff_number=staff_number,
            department=department,
            mobile_no=mobile_number,
            dateOf_Uni_Appointment=uni_appointment,
            designation_point=status.point,
            marital_status=marital_status,
            num_of_children=num_of_children,
        )
        if marital_status == "married" and marital_input:
            user.spouse_id = marital_input
        if bungalow_no:
            user.presentUni_bungalow = bungalow_no
        user.save() 
        staff_number = request.POST.get('staff_number')
        preference_count = int(request.POST.get('preference_count', 0))

        print(f"Staff Number: {staff_number}")
        print(f"Preference Count: {preference_count}")

        try:
            appointment = junior_staff_appointment.objects.get(staff_number=staff_number)
        except junior_staff_appointment.DoesNotExist:
            print("Appointment not found")
            return render(request, 'junior_staff.html', {'error': 'Appointment not found'})

        # Clear previous preferences for the same appointment
        Preference_junior_staff.objects.filter(application=appointment).delete()

        # Save preferences
        preferences_saved = 0
        for i in range(preference_count):
            preference_text = request.POST.get(f'preference_{i}')
            print(f"Preference {i}: {preference_text}")  # Debugging output
            print(junior_staff_appointment)
            if preference_text:
                Preference_junior_staff.objects.create(application=junior_staff_appointment, preference=preference_text)
                preferences_saved += 1
        
        print(f"Total Preferences Saved: {preferences_saved}")

        # Redirect or render success page
        return redirect('junior_staff')
    return render(request,'junior_staff.html')


#calculate points and assigned preferences based on points
import logging
def check_point(request):
    points = None
    marital_point = None
    accommodation_points = 0
    total = 0
    couples_point = 0

    all_appointments = list(Appointment.objects.all())
    all_senior_staff_appointments = list(senior_staff_appointment.objects.all())
    all_junior_staff_appointments = list(junior_staff_appointment.objects.all())

    results = []
    all_appointments_with_points = []
    aggregated_users = []
    couples = {}  # Dictionary to track processed couples

    def find_spouse_data(spouse_id, category):
        # Function to find spouse's data
        for app_data in all_appointments_with_points:
            if app_data['appointment'].staff_number == spouse_id and app_data['category'] == category:
                return app_data
        return None

    def determine_category(staff_number):
        if staff_number.startswith('js'):
            return 'junior_staff'
        elif staff_number.startswith('ss'):
            return 'senior_staff'
        elif staff_number.startswith('sm'):
            return 'senior_member'
        else:
            return 'unknown_category'

    def add_to_aggregated_users(name, staff_number, points, assigned_building='Not Assigned'):
        category = determine_category(staff_number)
        aggregated_users.append({
            'name': name,
            'staff_number': staff_number,
            'total_points': points,
            'assigned_building': assigned_building,
            'category': category
        })


    # Process junior staff appointments
    for junior_appointment in all_junior_staff_appointments:
        try:
            points = calculate_service_points_juniorstaff(
                junior_appointment.designation_point,
                junior_appointment.dateOf_Uni_Appointment.strftime('%Y-%m-%d')
            )
            marital_point = cal_marital_points_juniorstaff(
                junior_appointment.marital_status,
                junior_appointment.num_of_children
            )
            total = int(points) + int(marital_point)

            junior_appointment.total_points = total
            junior_appointment.save()

            staff_number = getattr(junior_appointment, 'staff_number', None)
            category = 'junior_staff'

            # Collect data for couples' points calculation
            all_appointments_with_points.append({
                'appointment': junior_appointment,
                'total_points': total,
                'category': category
            })

        except Exception as e:
            print(f'Error in processing junior staff appointment: {str(e)}')

    # Process senior staff appointments
    for staff_appointment in all_senior_staff_appointments:
        try:
            points = calculate_service_points_seniorstaff(
                staff_appointment.designation_point,
                staff_appointment.dateOf_Uni_Appointment.strftime('%Y-%m-%d')
            )
            marital_point = cal_marital_points_seniorstaff(
                staff_appointment.marital_status,
                staff_appointment.num_of_children
            )
            accommodation_points = calculate_present_accommodation_points_seniorstaff(
                staff_appointment.present_accommodation,
                staff_appointment.date_of_occupation_ofAccomodation.strftime('%Y-%m-%d') if staff_appointment.date_of_occupation_ofAccomodation else None
            ) if staff_appointment.present_accommodation else 0
            total = int(points) + int(marital_point) + int(accommodation_points)

            staff_appointment.total_points = total
            staff_appointment.save()

            category = 'senior_staff'

            # Collect data for couples' points calculation
            all_appointments_with_points.append({
                'appointment': staff_appointment,
                'total_points': total,
                'category': category
            })

        except Exception as e:
            print(f'Error in processing senior staff appointment: {str(e)}')

    # Process general appointments
    for appointment in all_appointments:
        try:
            points = calculate_status_points(
                appointment.initial_point,
                appointment.dateOf_Uni_Appointment.strftime('%Y-%m-%d'),
                appointment.studyLeave_from.strftime('%Y-%m-%d') if appointment.studyLeave_from else None,
                appointment.studyLeave_to.strftime('%Y-%m-%d') if appointment.studyLeave_to else None
            )
            marital_point = cal_marital_points(
                appointment.duty_status,
                appointment.marital_status,
                appointment.num_of_children,
                appointment.date_of_duty.strftime('%Y-%m-%d') if appointment.date_of_duty else None
            )
            accommodation_points = calculate_accommodation_points(
                appointment.present_accommodation,
                appointment.date_of_occupation_ofAccomodation.strftime('%Y-%m-%d') if appointment.date_of_occupation_ofAccomodation else None
            ) if appointment.present_accommodation else 0
            total = int(points) + int(marital_point) + int(accommodation_points)

            appointment.total_points = total
            appointment.save()

            category = 'senior_member'

            # Collect data for couples' points calculation
            all_appointments_with_points.append({
                'appointment': appointment,
                'total_points': total,
                'category': category
            })

        except Exception as e:
            print(f'Error in processing appointment: {str(e)}')

    # Calculate couples' points and aggregate data
    for entry in all_appointments_with_points:
        appointment = entry['appointment']
        category = entry['category']
        spouse_id = appointment.spouse_id
        if spouse_id and spouse_id not in couples:
            spouse_data = find_spouse_data(spouse_id, category)
            if spouse_data:
                spouse_name = spouse_data['appointment'].name
                # Aggregate couple data
                couple_name = f"{appointment.name} and {spouse_name}"
                couple_points = entry['total_points'] + spouse_data['total_points']
                couples[spouse_id] = True  # Mark spouse as processed
                couples[appointment.staff_number] = True  # Mark current user as processed
                add_to_aggregated_users(couple_name, f"{appointment.staff_number} & {spouse_data['appointment'].staff_number}", couple_points, "Not Assigned")
        elif appointment.staff_number not in couples:
            # Single users are added directly
            add_to_aggregated_users(appointment.name, appointment.staff_number, entry['total_points'], "Not Assigned")

    # Print aggregated users for debugging
    print(f'Aggregated users: {aggregated_users}')

    # Sort aggregated users by total points in descending order
    aggregated_users.sort(key=lambda x: x['total_points'], reverse=True)

    # Assign buildings based on sorted list
    for user in aggregated_users:
        # Get the category from user data or use a default value if necessary
        category = user.get('category')
        
        # Ensure that category is correctly set before passing it to assign_building
        if not category:
            # Handle the case where category might be missing
            print(f"Error: Missing category for user: {user}")
            category = 'unknown_category'  # Or another appropriate default

        print(f'Assigning building for category: {category}, Total Points: {user["total_points"]}')
        
        # Assign a building based on the category and total points
        assigned_building = assign_building(category, user['total_points'])
        print(f'Assigned Building: {assigned_building}')
        
        # Update results with assigned building
        user['assigned_building'] = assigned_building if assigned_building else 'Not Assigned'

        # Save assigned buildings to the appropriate table based on category
        save_assignment_to_db(user['staff_number'], assigned_building, user['total_points'], category)

        results.append(user)

    return render(request, 'check_point.html', {'results': results, 'couples_point': couples_point})

def save_assignment_to_db(staff_number, assigned_building, total_points, category):
    """Save or update assignment data in the appropriate table based on the category."""
    try:
        if category == 'senior_member':
            appointment = Appointment.objects.get(staff_number=staff_number)
            assign_preference, created = assign_point_and_preference.objects.get_or_create(
                application=appointment,
                defaults={'preference_assigned': assigned_building, 'total_points': total_points}
            )
            if not created:
                assign_preference.preference_assigned = assigned_building
                assign_preference.total_points = total_points
                assign_preference.save()

        elif category == 'senior_staff':
            appointment = senior_staff_appointment.objects.get(staff_number=staff_number)
            assign_preference, created = assign_point_and_preference_senior.objects.get_or_create(
                application=appointment,
                defaults={'preference_assigned': assigned_building, 'total_points': total_points}
            )
            if not created:
                assign_preference.preference_assigned = assigned_building
                assign_preference.total_points = total_points
                assign_preference.save()

        elif category == 'junior_staff':
            # Handle case where junior_staff_appointment does not exist
            try:
                appointment = junior_staff_appointment.objects.get(staff_number=staff_number)
                assign_preference, created = assign_point_and_preference_junior.objects.get_or_create(
                    application=appointment,
                    defaults={'preference_assigned': assigned_building, 'total_points': total_points}
                )
                if not created:
                    assign_preference.preference_assigned = assigned_building
                    assign_preference.total_points = total_points
                    assign_preference.save()
            except junior_staff_appointment.DoesNotExist:
                print(f"Error: junior_staff_appointment with staff_number {staff_number} does not exist.")
                # You can choose to handle this in another way, such as logging the error or returning

    except Exception as e:
        print(f"An error occurred while saving assignment to DB: {e}")

def assign_building(category, total_points):
    # Fetch available buildings based on category and ensure there are vacant rooms
    available_buildings = Building.objects.filter(category=category, vacant_rooms__gt=0).order_by('-vacant_rooms')
    print(f'Available buildings for category "{category}": {list(available_buildings)}')

    for building in available_buildings:
        if building.vacant_rooms > 0:
            print(f'Assigning building: {building.name}')
            building.vacant_rooms -= 1
            building.save()
            
            # Assuming assign_preference is relevant and needs to be updated
            # Make sure to add this part before returning if needed
            if 'assign_preference' in locals() and not created:
                assign_preference.preference_assigned = building.name
                assign_preference.total_points = total_points
                assign_preference.save()
            
            return building.name

    print('No building assigned.')
    return None
