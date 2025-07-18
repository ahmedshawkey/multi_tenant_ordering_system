from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework import status
from django.utils.timezone import now
import logging


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def product_list_create(request):
    user = request.user

    if request.method == 'GET':
        products = Product.objects.filter(company=user.company, is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if user.is_viewer():
            return Response({'error': 'Viewers cannot create products.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save(
                company=user.company,
                created_by=user
            )
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product_detail(request, pk):
    user = request.user

    try:
        product = Product.objects.get(pk=pk, company=user.company, is_active=True)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    user = request.user

    try:
        product = Product.objects.get(pk=pk, company=user.company)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    if user.role != 'admin':
        return Response({'error': 'Only admins can delete products.'}, status=status.HTTP_403_FORBIDDEN)

    product.is_active = False
    product.save()
    return Response({'message': 'Product marked as inactive.'}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def order_list_create(request):
    user = request.user

    if request.method == 'GET':
        orders = Order.objects.filter(company=user.company)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if user.is_viewer():
            return Response({'error': 'Viewers cannot place orders.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']

            if product.company != user.company or not product.is_active:
                return Response({'error': 'Invalid product for your company.'}, status=status.HTTP_400_BAD_REQUEST)

            if product.stock < quantity:
                return Response({'error': 'Insufficient stock.'}, status=status.HTTP_400_BAD_REQUEST)

            product.stock -= quantity
            product.save()

            order = serializer.save(
                company=user.company,
                created_by=user,
                status='pending'
            )

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_detail(request, pk):
    user = request.user

    try:
        order = Order.objects.get(pk=pk, company=user.company)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_order(request, pk):
    user = request.user

    try:
        order = Order.objects.get(pk=pk, company=user.company)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Restrict operators to same-day orders
    if user.role == 'operator' and order.created_at.date() != now().date():
        return Response({'error': 'Operators can only edit today’s orders.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = OrderSerializer(order, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


order_logger = logging.getLogger('order_email')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_order_shipped(request, pk):
    user = request.user

    try:
        order = Order.objects.get(pk=pk, company=user.company)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

    if order.status != 'pending':
        return Response({'error': 'Only pending orders can be marked as shipped.'}, status=status.HTTP_400_BAD_REQUEST)

    order.status = 'success'
    order.shipped_at = now()
    order.save()

    # 🧠 Log the simulated email
    order_logger.info(
        f"Order #{order.id} shipped. Confirmation sent to {order.created_by.email}. "
        f"Product: {order.product.name}, Quantity: {order.quantity}, Date: {now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    return Response({'message': 'Order marked as shipped and confirmation logged.'}, status=status.HTTP_200_OK)
