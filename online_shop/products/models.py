from django.db import models
from categories.models import Category


class Product(models.Model):
    product_name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    stock_quantity = models.PositiveIntegerField(default=0)
    product_image = models.URLField(
        max_length=500,
        default='https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400'
    )
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.product_name

    def get_effective_price(self):
        if self.discount_price and self.discount_price < self.price:
            return self.discount_price
        return self.price

    def get_discount_percentage(self):
        if self.discount_price and self.discount_price < self.price:
            discount = ((self.price - self.discount_price) / self.price) * 100
            return round(discount)
        return 0

    def is_in_stock(self):
        return self.stock_quantity > 0

    def update_rating(self):
        from reviews.models import Review
        reviews = Review.objects.filter(product=self)
        if reviews.exists():
            avg = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.rating = round(avg, 2)
        else:
            self.rating = 0
        self.save()