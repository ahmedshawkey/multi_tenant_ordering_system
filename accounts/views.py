from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework import status


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
