import os
import django
from django.db.models import Q, Count, F

from main_app.models import Profile, Order, Product

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


def get_profiles(search_string=None):
    if search_string is None:
        return ""

    profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string)
            |
        Q(email__icontains=search_string)
            |
        Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    return '\n'.join(
        f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.orders.count()}"
        for p in profiles
    )


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    return '\n'.join(
        f'Profile: {p.full_name}, orders: {p.orders_count}'
        for p in profiles
    )


def get_last_sold_products():
    last_order = Order.objects.prefetch_related('products').last()

    if last_order is None or not last_order.products.exists():
        return ""

    product_names = [product.name for product in last_order.products.all()]

    return f"Last sold products: {', '.join(product_names)}"


def get_top_products() -> str:
    top_products = (Product.objects.annotate(
        num_orders=Count('order')
    ).filter(
        num_orders__gt=0
    ).order_by(
        '-num_orders',
        'name'
         )
    )[:5]

    if not top_products:
        return ""

    result = [f'{product.name}, sold {product.num_orders} times' for product in top_products]

    return f"Top products:\n" + "\n".join(result)


def apply_discounts():
    updated_orders = Order.objects.annotate(
        products_count=Count('products')
    ).filter(
        products_count__gt=2,
        is_completed=False,
    ).update(
        total_price=F('total_price') * 0.90
    )

    return f'Discount applied to {updated_orders} orders.'


def complete_order():
    order = Order.objects.prefetch_related('products').filter(
        is_completed=False
    ).order_by(
        'creation_date'
    ).first()

    if not order:
        return ""

    for product in order.products.all():
        product.in_stock -= 1

        if product.in_stock == 0:
            product.is_available = False

        product.save()

    order.is_completed = True
    order.save()

    return f'Order has been completed!'
