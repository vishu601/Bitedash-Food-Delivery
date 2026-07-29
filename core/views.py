from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import FoodItem, Order, DeliveryLocation
from .forms import SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('menu')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('menu')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# Menu View
def menu_view(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    food_items = FoodItem.objects.filter(is_available=True)
    if query:
        food_items = food_items.filter(name__icontains=query)
    if category and category != 'All':
        food_items = food_items.filter(category=category)
        
    return render(request, 'core/menu.html', {'food_items': food_items})

# Cart View (Session based)
def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    request.session['cart'] = cart
    return redirect('menu')

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for item_id, quantity in cart.items():
        item = get_object_or_404(FoodItem, id=item_id)
        subtotal = item.price * quantity
        total_price += subtotal
        cart_items.append({'item': item, 'quantity': quantity, 'subtotal': subtotal})
        
    return render(request, 'core/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required(login_url='/login/')
def place_order(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        cart = request.session.get('cart', {})
        
        if not cart:
            return redirect('menu')
            
        total_price = sum(get_object_or_404(FoodItem, id=i_id).price * qty for i_id, qty in cart.items())
        
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            delivery_address=address,
            status='Placed'
        )
        
        DeliveryLocation.objects.create(order=order, latitude=28.6139, longitude=77.2090)
        
        # Clear cart
        request.session['cart'] = {}
        return redirect('order_success', order_id=order.id)
    return redirect('cart')

@login_required(login_url='/login/')
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'core/track_order.html', {'order': order})