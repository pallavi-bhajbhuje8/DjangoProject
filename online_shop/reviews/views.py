from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from products.models import Product


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    existing_review = Review.objects.filter(product=product, user=request.user).first()
    if existing_review:
        messages.warning(request, 'You have already reviewed this product. You can edit your review.')
        return redirect('products:product_detail', slug=product.slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            product.update_rating()
            messages.success(request, 'Review added successfully!')
    return redirect('products:product_detail', slug=product.slug)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            review.product.update_rating()
            messages.success(request, 'Review updated successfully!')
    return redirect('products:product_detail', slug=review.product.slug)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product = review.product
    review.delete()
    product.update_rating()
    messages.success(request, 'Review deleted.')
    return redirect('products:product_detail', slug=product.slug)