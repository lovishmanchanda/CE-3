from django.shortcuts import render ,redirect, get_object_or_404
from .forms import CareTipForm, HospitalForm, FoodForm, ClothesForm, MedicineForm, AccessoryForm
from .models import Food, Clothes, Medicine, Hospital, Accessory, CareTip
from django.contrib.auth.decorators import login_required
from .models import CartItem
from .utils import get_product_instance
from django.contrib import messages
from .utils import get_product_by_category
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required



# --- Pet Care Tips ---

@staff_member_required
def add_tip(request):
    if request.method == 'POST':
        form = CareTipForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_tip')  # Stay on same page to see added tips
    else:
        form = CareTipForm()
    
    tips = CareTip.objects.all()  # 🔸 Add this line
    return render(request, 'petcare/add_tip.html', {
        'form': form,
        'tips': tips  # 🔸 Pass tips to template
    })

def view_tips(request):
    tips = CareTip.objects.all()
    return render(request, 'petcare/view_tips.html', {'tips': tips})

@staff_member_required
def delete_tip(request, tip_id):
    tip = get_object_or_404(CareTip, id=tip_id)
    tip.delete()
    return redirect('add_tip')  # Redirect to the list of tips after deletion


# --- Hospital ---

@staff_member_required
def add_hospital(request):
    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_hospitals')
    else:
        form = HospitalForm()
    return render(request, 'petcare/add_hospital.html', {'form': form})

def view_hospitals(request):
    hospitals = Hospital.objects.all()
    return render(request, 'petcare/view_hospitals.html', {'hospitals': hospitals})


# --- Food ---

@staff_member_required
def add_food(request):
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_food')  # Same page refresh
    else:
        form = FoodForm()

    food_items = Food.objects.all()  # ✅ Add this to show list of foods

    return render(request, 'petcare/add_food.html', {
        'form': form,
        'food_items': food_items,
    })

def view_food(request):
    food_items = Food.objects.all()
    return render(request, 'petcare/view_food.html', {'food_items': food_items})

@login_required
def delete_food(request, item_id):
    item = get_object_or_404(Food, id=item_id)
    item.delete()
    return redirect('add_food')  # Back to the same admin page




# --- Clothes ---

@staff_member_required
def add_clothes(request):
    if request.method == 'POST':
        form = ClothesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_clothes')  # Refreshes same page
    else:
        form = ClothesForm()

    clothes = Clothes.objects.all()  # ✅ List of added clothes

    return render(request, 'petcare/add_clothes.html', {
        'form': form,
        'clothes': clothes,
    })

def view_clothes(request):
    clothes = Clothes.objects.all()
    return render(request, 'petcare/view_clothes.html', {'clothes': clothes})

@login_required
def delete_clothes(request, item_id):
    item = get_object_or_404(Clothes, id=item_id)
    item.delete()
    return redirect('add_clothes')  # ✅ Back to same admin page


# --- Medicines ---

@staff_member_required
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_medicines')
    else:
        form = MedicineForm()

    medicines = Medicine.objects.all()

    return render(request, 'petcare/add_medicine.html', {
        'form': form,
        'medicines': medicines,
    })

def view_medicines(request):
    medicines = Medicine.objects.all()
    return render(request, 'petcare/view_medicines.html', {'medicines': medicines})

@login_required
def delete_medicine(request, item_id):
    item = get_object_or_404(Medicine, id=item_id)
    item.delete()
    return redirect('view_medicines')


# --- Accessories ---

@user_passes_test(lambda u: u.is_superuser)
def add_accessory(request):
    if request.method == 'POST':
        form = AccessoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_accessory')  # stay on same page
    else:
        form = AccessoryForm()
    
    accessories = Accessory.objects.all()
    return render(request, 'petcare/add_accessory.html', {
        'form': form,
        'accessories': accessories
    })

def view_accessories(request):
    accessories = Accessory.objects.all()
    return render(request, 'petcare/view_accessories.html', {'accessories': accessories})

@user_passes_test(lambda u: u.is_superuser)
def delete_accessory(request, item_id):
    accessory = get_object_or_404(Accessory, id=item_id)
    accessory.delete()
    return redirect('add_accessory')



#  home page

def petcare_home(request):
    return render(request, 'petcare/home.html')

#  cart item 

@login_required
def add_to_cart(request, category, product_id):
    cart = request.session.get('cart', {})

    product = get_product_by_category(category, product_id)
    if not product:
        messages.error(request, f"No product found for {category} with ID {product_id}")
        return redirect('cart')

    product_key = f"{category}_{product_id}"

    if product_key in cart:
        cart[product_key]['quantity'] += 1
    else:
        cart[product_key] = {
            'product_id': product.id,
            'category': category,
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
        }

    request.session['cart'] = cart  # 🔥 Don't forget this!
    messages.success(request, f"{product.name} Added to cart✅.")
    return redirect('view_cart')  # or redirect wherever you want

#  cart 
@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for key, item in cart.items():
        item['item_key'] = key  # Needed for URL operations in template
        subtotal = item['price'] * item['quantity']
        item['subtotal'] = subtotal
        total += subtotal
        cart_items.append(item)

    return render(request, 'petcare/cart.html', {
        'items': cart_items,
        'total': total
    })



@login_required
def update_cart_item(request, item_key, action):
    cart = request.session.get('cart', {})

    if item_key in cart:
        if action == 'increase':
            cart[item_key]['quantity'] += 1
        elif action == 'decrease':
            cart[item_key]['quantity'] -= 1
            if cart[item_key]['quantity'] <= 0:
                del cart[item_key]

        request.session['cart'] = cart
        messages.success(request, "Cart updated.")

    return redirect('view_cart')


@login_required
def remove_cart_item(request, item_key):
    cart = request.session.get('cart', {})
    
    if item_key in cart:
        del cart[item_key]
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")
    
    return redirect('view_cart')


#  for viewing products
def view_food_detail(request, pk):
    food = get_object_or_404(Food, pk=pk)
    return render(request, 'petcare/food_detail.html', {'food': food})

def view_medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    return render(request, 'petcare/medicine_detail.html', {'medicine': medicine})

def view_accessory_detail(request, pk):
    accessory = get_object_or_404(Accessory, pk=pk)
    return render(request, 'petcare/accessory_detail.html', {'accessory': accessory})

def view_cloth_detail(request, pk):
    cloth = get_object_or_404(Clothes, pk=pk)
    return render(request, 'petcare/cloth_detail.html', {'cloth': cloth})


#  payment gateways 

@login_required
def fake_payment(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for item in cart.values():
        subtotal = item['price'] * item['quantity']
        item['subtotal'] = subtotal
        total += subtotal
        cart_items.append(item)

    # Clear cart after showing summary
    request.session['cart'] = {}

    return render(request, 'petcare/fake_payment.html', {
        'items': cart_items,
        'total': total
    })

def home(request):
    return render(request, 'petcare/home.html')