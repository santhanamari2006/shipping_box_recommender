from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from django.contrib.auth import (
    login,
    logout,
    authenticate,
    get_user_model
)

from django.contrib.auth.decorators import (
    login_required,
    user_passes_test
)

from django.contrib.admin.views.decorators import staff_member_required

from .models import Product, Order, OrderItem
from .forms import RegisterForm
from .packing import calculate_packing


# HOME PAGE
def home(request):
    return render(request, "packaging/home.html")


# CUSTOMER REGISTRATION
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("product_list")
    else:
        form = RegisterForm()

    return render(
        request,
        "packaging/register.html",
        {"form": form}
    )


# CUSTOMER PRODUCT LIST
@login_required
def product_list(request):
    if request.user.is_staff:
        return redirect("warehouse_dashboard")

    products = Product.objects.all().order_by("id")

    paginator = Paginator(products, 3)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "packaging/product_list.html",
        {"page_obj": page_obj}
    )

# CUSTOMER LOGIN
def customer_login(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_active and not user.is_staff:
            login(request, user)
            return redirect("product_list")

        error = "Invalid customer username or password."

    return render(
        request,
        "packaging/login.html",
        {"error": error}
    )

# CREATE PACKAGING STAFF ACCOUNT
@user_passes_test(
    lambda user: user.is_authenticated and user.is_superuser,
    login_url="/admin/login/"
)
def create_staff(request):
    error = ""
    success = ""

    User = get_user_model()

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username or not password or not confirm_password:
            error = "Please fill in all fields."

        elif User.objects.filter(username=username).exists():
            error = "Username already exists."

        elif password != confirm_password:
            error = "Passwords do not match."

        else:
            User.objects.create_user(
                username=username,
                password=password,
                is_staff=True,
                is_superuser=False
            )

            success = (
                "Packaging staff account created successfully. "
                "The staff member can now use Staff Login."
            )

    return render(
        request,
        "packaging/create_staff.html",
        {
            "error": error,
            "success": success
        }
    )


# PACKAGING STAFF LOGIN
def staff_login(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if (
            user is not None
            and user.is_active
            and user.is_staff
            and not user.is_superuser
        ):
            login(request, user)
            return redirect("warehouse_dashboard")

        error = "Invalid staff username or password."

    return render(
        request,
        "packaging/staff_login.html",
        {"error": error}
    )


# PACKAGING STAFF DASHBOARD
@staff_member_required(login_url="staff_login")
def warehouse_dashboard(request):
    if request.user.is_superuser:
        return redirect("/admin/")

    orders = (
        Order.objects
        .filter(is_completed=True)
        .select_related("user")
        .prefetch_related("items__product")
        .order_by("-created_at")
    )

    return render(
        request,
        "packaging/warehouse_dashboard.html",
        {"orders": orders}
    )


# CUSTOMER BUYS PRODUCT
@login_required
def buy_product(request, product_id):
    if request.method != "POST":
        return redirect("product_list")

    if request.user.is_staff:
        return redirect("warehouse_dashboard")

    product = get_object_or_404(Product, id=product_id)

    order = Order.objects.filter(
        user=request.user,
        is_completed=False
    ).first()

    if order is None:
        order = Order.objects.create(user=request.user)

    item = OrderItem.objects.filter(
        order=order,
        product=product
    ).first()

    if item:
        item.quantity += 1
        item.save()
    else:
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price=product.price
        )

    return render(
        request,
        "packaging/purchase_question.html",
        {"product": product}
    )


# CUSTOMER FINISHES PURCHASE
@login_required
def finish_purchase(request):
    if request.method != "POST":
        return redirect("product_list")

    if request.user.is_staff:
        return redirect("warehouse_dashboard")

    choice = request.POST.get("choice")

    order = get_object_or_404(
        Order,
        user=request.user,
        is_completed=False
    )

    if choice == "yes":
        order.is_completed = True
        order.save()

        return redirect(
            "order_summary",
            order_id=order.id
        )

    if choice == "no":
        return redirect("product_list")

    return redirect("product_list")


# CUSTOMER ORDER SUMMARY
@login_required
def order_summary(request, order_id):
    if request.user.is_staff:
        return redirect("warehouse_dashboard")

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
        is_completed=True
    )

    return render(
        request,
        "packaging/order_summary.html",
        {"order": order}
    )


# PACKAGING STAFF CALCULATES SHIPPING BOXES
@staff_member_required(login_url="staff_login")
def warehouse_packing(request, order_id):
    if request.user.is_superuser:
        return redirect("/admin/")

    order = get_object_or_404(
        Order,
        id=order_id,
        is_completed=True
    )

    try:
        packed_boxes = calculate_packing(order)

        total_box_cost = sum(
            float(packed_box["box"].cost)
            for packed_box in packed_boxes
        )

        return render(
            request,
            "packaging/warehouse_packing.html",
            {
                "order": order,
                "packed_boxes": packed_boxes,
                "total_box_cost": total_box_cost
            }
        )

    except ValueError as error:
        return render(
            request,
            "packaging/warehouse_packing.html",
            {
                "order": order,
                "error": str(error)
            }
        )


# LOGOUT
@login_required
def user_logout(request):
    if request.method == "POST":
        logout(request)

    return redirect("home")
