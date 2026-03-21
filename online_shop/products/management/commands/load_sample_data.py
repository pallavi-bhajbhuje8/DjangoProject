import os
import django

from django.core.management.base import BaseCommand
from categories.models import Category
from products.models import Product
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Load sample data into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading sample data...')

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superuser created: admin / admin123'))

        # Create sample users
        sample_users = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
        ]
        for u_data in sample_users:
            if not User.objects.filter(username=u_data['username']).exists():
                user = User.objects.create_user(
                    username=u_data['username'],
                    email=u_data['email'],
                    password='password123',
                    first_name=u_data['first_name'],
                    last_name=u_data['last_name']
                )
                self.stdout.write(f"User created: {u_data['username']}")

        # Create categories
        categories_data = [
            {
                'name': 'Electronics',
                'slug': 'electronics',
                'description': 'Latest electronic gadgets and devices',
                'image': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400',
            },
            {
                'name': 'Clothing',
                'slug': 'clothing',
                'description': 'Trendy fashion and clothing',
                'image': 'https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=400',
            },
            {
                'name': 'Footwear',
                'slug': 'footwear',
                'description': 'Comfortable and stylish footwear',
                'image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400',
            },
            {
                'name': 'Books',
                'slug': 'books',
                'description': 'Books across all genres',
                'image': 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400',
            },
            {
                'name': 'Home Appliances',
                'slug': 'home-appliances',
                'description': 'Essential home appliances',
                'image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400',
            },
            {
                'name': 'Fitness Equipment',
                'slug': 'fitness-equipment',
                'description': 'Gym and fitness equipment',
                'image': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400',
            },
        ]

        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f"Category created: {cat.name}")

        # Create products
        products_data = [
            {
                'product_name': 'MacBook Pro 16"',
                'slug': 'macbook-pro-16',
                'description': 'Apple MacBook Pro 16-inch with M2 Pro chip, 16GB RAM, 512GB SSD. Perfect for professionals and creators.',
                'price': 2499.99,
                'discount_price': 2299.99,
                'category': 'electronics',
                'stock_quantity': 25,
                'product_image': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400',
                'rating': 4.8,
                'is_featured': True,
            },
            {
                'product_name': 'iPhone 15 Pro',
                'slug': 'iphone-15-pro',
                'description': 'Apple iPhone 15 Pro with A17 Pro chip, 48MP camera, and titanium design.',
                'price': 1199.99,
                'discount_price': 1099.99,
                'category': 'electronics',
                'stock_quantity': 50,
                'product_image': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400',
                'rating': 4.7,
                'is_featured': True,
            },
            {
                'product_name': 'Samsung Galaxy S24 Ultra',
                'slug': 'samsung-galaxy-s24-ultra',
                'description': 'Samsung Galaxy S24 Ultra with S Pen, 200MP camera, and AI features.',
                'price': 1299.99,
                'discount_price': 1199.99,
                'category': 'electronics',
                'stock_quantity': 40,
                'product_image': 'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400',
                'rating': 4.6,
                'is_featured': True,
            },
            {
                'product_name': 'Sony WH-1000XM5 Headphones',
                'slug': 'sony-wh1000xm5',
                'description': 'Industry-leading noise cancelling wireless headphones with exceptional sound quality.',
                'price': 399.99,
                'discount_price': 349.99,
                'category': 'electronics',
                'stock_quantity': 100,
                'product_image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
                'rating': 4.5,
                'is_featured': False,
            },
            {
                'product_name': 'Classic Denim Jacket',
                'slug': 'classic-denim-jacket',
                'description': 'Timeless denim jacket with a modern fit. Perfect for casual outings.',
                'price': 89.99,
                'discount_price': 69.99,
                'category': 'clothing',
                'stock_quantity': 200,
                'product_image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400',
                'rating': 4.3,
                'is_featured': True,
            },
            {
                'product_name': 'Premium Cotton T-Shirt',
                'slug': 'premium-cotton-tshirt',
                'description': 'Ultra-soft premium cotton t-shirt. Available in multiple colors.',
                'price': 29.99,
                'discount_price': 24.99,
                'category': 'clothing',
                'stock_quantity': 500,
                'product_image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
                'rating': 4.2,
                'is_featured': False,
            },
            {
                'product_name': 'Nike Air Max 270',
                'slug': 'nike-air-max-270',
                'description': 'Nike Air Max 270 with the biggest heel Air unit yet for a super-soft ride.',
                'price': 150.00,
                'discount_price': 129.99,
                'category': 'footwear',
                'stock_quantity': 75,
                'product_image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400',
                'rating': 4.6,
                'is_featured': True,
            },
            {
                'product_name': 'Adidas Ultraboost 22',
                'slug': 'adidas-ultraboost-22',
                'description': 'Adidas Ultraboost running shoes with responsive Boost midsole.',
                'price': 180.00,
                'discount_price': 159.99,
                'category': 'footwear',
                'stock_quantity': 60,
                'product_image': 'https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400',
                'rating': 4.5,
                'is_featured': False,
            },
            {
                'product_name': 'The Pragmatic Programmer',
                'slug': 'pragmatic-programmer',
                'description': 'A classic software development book covering tips and best practices for programmers.',
                'price': 49.99,
                'discount_price': 39.99,
                'category': 'books',
                'stock_quantity': 300,
                'product_image': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400',
                'rating': 4.9,
                'is_featured': True,
            },
            {
                'product_name': 'Clean Code',
                'slug': 'clean-code',
                'description': 'A Handbook of Agile Software Craftsmanship by Robert C. Martin.',
                'price': 44.99,
                'discount_price': 37.99,
                'category': 'books',
                'stock_quantity': 250,
                'product_image': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400',
                'rating': 4.8,
                'is_featured': False,
            },
            {
                'product_name': 'Robot Vacuum Cleaner',
                'slug': 'robot-vacuum-cleaner',
                'description': 'Smart robot vacuum cleaner with mapping technology and app control.',
                'price': 499.99,
                'discount_price': 399.99,
                'category': 'home-appliances',
                'stock_quantity': 30,
                'product_image': 'https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=400',
                'rating': 4.4,
                'is_featured': True,
            },
            {
                'product_name': 'Air Purifier Pro',
                'slug': 'air-purifier-pro',
                'description': 'HEPA air purifier for rooms up to 500 sq ft. Removes 99.97% of particles.',
                'price': 299.99,
                'discount_price': 249.99,
                'category': 'home-appliances',
                'stock_quantity': 45,
                'product_image': 'https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400',
                'rating': 4.3,
                'is_featured': False,
            },
            {
                'product_name': 'Adjustable Dumbbell Set',
                'slug': 'adjustable-dumbbell-set',
                'description': 'Adjustable dumbbells from 5 to 52.5 lbs. Perfect for home workouts.',
                'price': 349.99,
                'discount_price': 299.99,
                'category': 'fitness-equipment',
                'stock_quantity': 35,
                'product_image': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400',
                'rating': 4.7,
                'is_featured': True,
            },
            {
                'product_name': 'Yoga Mat Premium',
                'slug': 'yoga-mat-premium',
                'description': 'Extra thick premium yoga mat with non-slip surface. 6mm thickness.',
                'price': 49.99,
                'discount_price': 39.99,
                'category': 'fitness-equipment',
                'stock_quantity': 150,
                'product_image': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400',
                'rating': 4.4,
                'is_featured': False,
            },
        ]

        for p_data in products_data:
            cat_slug = p_data.pop('category')
            try:
                category = Category.objects.get(slug=cat_slug)
                product, created = Product.objects.get_or_create(
                    slug=p_data['slug'],
                    defaults={**p_data, 'category': category}
                )
                if created:
                    self.stdout.write(f"Product created: {product.product_name}")
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"Category '{cat_slug}' not found for product '{p_data['product_name']}'")
                )

        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))