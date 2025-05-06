from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Pet, Wishlist
from django.http import HttpResponseForbidden, Http404
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models import Pet, Wishlist
import requests
from django.conf import settings



AppUser = get_user_model()

# Create your views here.
def home_view(request):
    return render(request, 'index.html')

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')

def pets_view(request):
    # Fetch Django pets
    django_pets = Pet.objects.all()

    # Fetch Flask pets from API
    flask_api_url = f"{settings.FLASK_API_BASE_URL}/pets/all"
    try:
        response = requests.get(flask_api_url)
        flask_pets = response.json() if response.status_code == 200 else []
        for pet in flask_pets:
            filename = pet.get("image_filename")
            pet["image_url"] = f"http://localhost:5000/static/images/{filename}"
    except Exception as e:
        print(f"Error fetching Flask API pets: {e}")
        flask_pets = []

    context = {
        'django_pets': django_pets,
        'flask_pets': flask_pets
    }
    return render(request, 'pets.html', context)


@login_required
def pet_profile_view(request, source, pet_id):
    is_flask_pet = (source == 'flask')

    if is_flask_pet:
        flask_api_url = f"{settings.FLASK_API_BASE_URL}/pets/view/{pet_id}"  # Ensure the correct endpoint
        try:
            response = requests.get(flask_api_url)
            if response.status_code == 200:
                pet = response.json()

                # Add image_url key like in the pets_view
                filename = pet.get("image_filename")
                if filename:
                    pet["image_url"] = f"http://localhost:5000/static/images/{filename}"
            else:
                raise Http404("Pet not found in Flask API")
        except Exception as e:
            print(f"Error fetching Flask API pet: {e}")
            raise Http404("Pet not found")
        is_owner = False
        in_wishlist = False
    else:
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            raise Http404("Pet not found in local DB")

        is_owner = pet.owner == request.user
        in_wishlist = Wishlist.objects.filter(user=request.user, pet=pet).exists()

    context = {
        'pet': pet,
        'is_owner': is_owner,
        'in_wishlist': in_wishlist,
        'is_flask_pet': is_flask_pet
    }
    return render(request, 'pet_profile.html', context)


@login_required
def add_pet_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        breed = request.POST.get('breed')
        age = request.POST.get('age')
        pet_type = request.POST.get('pet_type')
        other_pet_type = request.POST.get('other_pet_type')
        description = request.POST.get('description')
        medical_issues = request.POST.get('medical_issues')
        address = request.POST.get('address')
        image = request.FILES.get('image')

        # Handle "Other" pet type
        pet_type_final = other_pet_type if pet_type == 'Other' and other_pet_type else pet_type

        try:
            pet = Pet.objects.create(
                name=name,
                breed=breed,
                age=age,
                pet_type=pet_type_final,
                other_pet_type=other_pet_type if pet_type == 'Other' else '',
                description=description,
                medical_issues=medical_issues,
                address=address,
                image=image,
                owner=request.user
            )
            messages.success(request, f"{pet.name} has been added successfully!")
            return redirect('profile')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'add_pet.html')

@login_required
def edit_pet_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)

    if request.method == 'POST':
        pet.name = request.POST.get('name')
        pet.breed = request.POST.get('breed')
        pet.age = request.POST.get('age')
        pet.pet_type = request.POST.get('pet_type')

        # Only save 'other_pet_type' if selected type is 'Other'
        pet.other_pet_type = request.POST.get('other_pet_type') if pet.pet_type == 'Other' else ''

        pet.description = request.POST.get('description')
        pet.medical_issues = request.POST.get('medical_issues')
        pet.address = request.POST.get('address')

        # Handle image upload
        if 'image' in request.FILES:
            pet.image = request.FILES['image']

        pet.save()
        messages.success(request, "Pet details updated successfully!")
        return redirect('pet_profile', pet_id=pet.id)

    return render(request, 'edit_pet.html', {'pet': pet})

@login_required
def manage_pets_view(request):
    if not request.user.is_superuser:  # Only allow superusers to access this view
        return redirect('home')

    pets = Pet.objects.all()
    return render(request, 'manage_pets.html', {'pets': pets})


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('pet')
    pets = [item.pet for item in wishlist_items]
    return render(request, 'wishlist.html', {'pets': pets})


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            # messages.success(request, f"Welcome back, {user.name}!")

            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect(request.GET.get('next') or 'home')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone = request.POST['phone']
        address = request.POST['address']
        gender = request.POST['gender']

        # Validation checks
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if AppUser.objects.filter(email=email).exists():
            messages.warning(request, "Email is already registered.")
            return redirect('register')

        # Create the user
        user = AppUser.objects.create(
            name=name,
            email=email,
            password=make_password(password),
            phone=phone,
            address=address,
            gender=gender,
        )
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')

    return render(request, 'register.html')

def profile_view(request):
    return render(request, 'profile.html')

@login_required
def edit_profile_view(request):
    user = request.user  # Get the currently logged-in user

    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')

        user.name = name
        user.phone = request.POST.get('mobile')
        user.save()

        messages.success(request, "Your profile has been updated successfully.")
        return redirect('profile')  # Redirect to profile page after update

    return render(request, 'edit_profile.html', {'user': user})

def privacy_view(request):
    return render(request, 'privacy.html')

def terms_view(request):
    return render(request, 'terms.html')

@login_required
def admin_dashboard_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to access the admin dashboard.")

    return render(request, 'admin_dashboard.html')


@login_required
def manage_users_view(request):
    users = AppUser.objects.all()  # ✅ Queryset: list of users
    return render(request, 'manage_users.html', {'users': users})

@login_required
def delete_user_view(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('home')

    User = get_user_model()
    user = get_object_or_404(User, id=user_id)

    # Prevent deletion of another superuser
    if user.is_superuser:
        messages.error(request, "You cannot delete a superuser.")
        return redirect('manage_users')

    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('manage_users')

# DELETE PET
# -------------------------
@login_required
def delete_pet_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.user != pet.owner:
        return HttpResponseForbidden("You are not authorized to delete this pet.")

    if request.method == "POST":
        pet.delete()
        messages.success(request, "Pet deleted successfully.")
        return redirect('manage_pets')  # or wherever you list the owner's pets

    return render(request, 'confirm_delete.html', {'pet': pet})



# -------------------------
# ADD TO WISHLIST
# -------------------------
@login_required
def add_to_wishlist_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    # Check if already in wishlist
    if Wishlist.objects.filter(user=request.user, pet=pet).exists():
        messages.info(request, "Pet is already in your wishlist.")
    else:
        Wishlist.objects.create(user=request.user, pet=pet)  # ✅ Make sure this pet is valid
        messages.success(request, "Pet added to your wishlist!")

    return redirect('wishlist')

@login_required
def remove_from_wishlist_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, pet=pet).first()
    if wishlist_item:
        wishlist_item.delete()
        messages.success(request, "Pet removed from your wishlist.")
    else:
        messages.warning(request, "This pet is not in your wishlist.")
    return redirect('wishlist')



def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


# ADOPT PET
# -------------------------
@login_required
def adopt_pet_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if pet.status != 'Available':
        messages.warning(request, "This pet is not available for adoption.")
        return redirect('pet_profile', pet_id=pet_id)

    if request.method == 'POST':
        pet.status = 'Under Review'  # Or 'Adopted', depending on your logic
        pet.save()
        messages.success(request, f"You've submitted an adoption request for {pet.name}.")
        return redirect('pet_profile', pet_id=pet.id)

    return redirect('pet_profile', pet_id=pet.id)


# @login_required
# def manageflask(request):
#     # Ensure the user is an admin
#     if not request.user.is_staff:
#         raise Http404("Not authorized")

#     flask_api_url = f"{settings.FLASK_API_BASE_URL}/pets/all"
#     try:
#         response = requests.get(flask_api_url)
#         if response.status_code == 200:
#             flask_pets = response.json()
#         else:
#             flask_pets = []
#     except Exception as e:
#         print(f"Error fetching Flask API pets: {e}")
#         flask_pets = []

#     context = {
#         'flask_pets': flask_pets
#     }
#     return render(request, 'ManageFlask.html', context)

# Admin check decorator
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@login_required
@admin_required
def manageflask(request):
    flask_api_url = f"{settings.FLASK_API_BASE_URL}/pets/all"
    try:
        response = requests.get(flask_api_url)
        flask_pets = response.json() if response.status_code == 200 else []
    except Exception as e:
        print(f"Error fetching Flask pets: {e}")
        flask_pets = []
    return render(request, 'ManageFlask.html', {'flask_pets': flask_pets})

@login_required
@admin_required
def addflask(request):
    if request.method == 'POST':
        try:
            # Prepare form data
            form_data = {
                'name': request.POST.get('name'),
                'breed': request.POST.get('breed'),
                'age': request.POST.get('age'),
                'pet_type': request.POST.get('pet_type'),
                'other_pet_type': request.POST.get('other_pet_type'),
                'description': request.POST.get('description'),
                'medical_issues': request.POST.get('medical_issues'),
                'address': request.POST.get('address'),
            }

            # Prepare file data (image)
            image_file = request.FILES.get('image')
            files = {}
            if image_file:
                files['image'] = (image_file.name, image_file, image_file.content_type)

            # Send POST request to Flask API
            response = requests.post(
                f"{settings.FLASK_API_BASE_URL}/pets",
                data=form_data,
                files=files
            )

            if response.status_code == 201:
                messages.success(request, "Pet added successfully!")
                return redirect('manageflask')
            else:
                print("API error:", response.status_code, response.text)  # DEBUG
                messages.error(request, f"Failed to add pet: {response.json().get('error', 'Unknown error')}")

        except Exception as e:
            print("Exception:", e)
            messages.error(request, "An error occurred while adding the pet.")
    
    return render(request, 'addflask.html')

@login_required
@admin_required
def editflask(request, pet_id):
    get_url = f"{settings.FLASK_API_BASE_URL}/pets/view/{pet_id}"
    update_url = f"{settings.FLASK_API_BASE_URL}/pets/edit/{pet_id}"

    if request.method == "POST":
        data = {
            "name": request.POST.get("name"),
            "breed": request.POST.get("breed"),
            "age": request.POST.get("age"),
            "status": request.POST.get("status"),
            "pet_type": request.POST.get("pet_type"),
            "other_pet_type": request.POST.get("other_pet_type"),
            "description": request.POST.get("description"),
            "medical_issues": request.POST.get("medical_issues"),
            "address": request.POST.get("address"),
        }

        # Handle image upload if present
        if 'image' in request.FILES:
            image = request.FILES['image']
            data['image'] = image

        try:
            # Send data to Flask API to update the pet
            response = requests.put(update_url, data=data)
            if response.status_code == 200:
                messages.success(request, "Pet updated successfully!")
            else:
                messages.error(request, "Failed to update pet.")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect('manageflask')

    try:
        # Fetch pet details from Flask API
        response = requests.get(get_url)
        if response.status_code == 200:
            pet = response.json()
        else:
            raise Http404("Pet not found")
    except Exception as e:
        print(f"Error fetching pet: {e}")
        raise Http404("Pet not found")

    pet_types = ['Dog', 'Cat', 'Bird', 'Horse']
    
    return render(request, 'editflask.html', {
        'pet': pet,  # Passing pet data
        'pet_types': pet_types,
        'flask_image_url': 'http://localhost:5000/static/uploads'  # Update with the correct image URL path
    })

@login_required
@admin_required
def deleteflask(request, pet_id):
    delete_url = f"{settings.FLASK_API_BASE_URL}/pets/delete/{pet_id}"
    try:
        response = requests.delete(delete_url)
        if response.status_code == 200:
            messages.success(request, "Pet deleted successfully!")
        else:
            messages.error(request, "Failed to delete pet.")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('manageflask')