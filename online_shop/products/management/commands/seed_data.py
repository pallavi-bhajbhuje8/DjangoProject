from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from categories.models import Category
from products.models import Product
from users.models import UserProfile


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding categories...')
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
                'description': 'Trendy fashion and apparel',
                'image': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400',
            },
            {
                'name': 'Footwear',
                'slug': 'footwear',
                'description': 'Shoes, sneakers, and boots',
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
                'description': 'Gym and fitness gear',
                'image': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400',
            },
        ]

        for cat_data in categories_data:
            Category.objects.get_or_create(slug=cat_data['slug'], defaults=cat_data)

        self.stdout.write('Seeding products...')
        products_data = [
            {
                'product_name': 'MacBook Pro 16"',
                'slug': 'macbook-pro-16',
                'description': 'Apple MacBook Pro 16-inch with M2 Pro chip, 16GB RAM, 512GB SSD. Perfect for professionals and creatives who need powerful computing on the go.',
                'price': 2499.99,
                'discount_price': 2299.99,
                'category_slug': 'electronics',
                'stock_quantity': 25,
                'product_image': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400',
                'rating': 4.8,
                'is_featured': True,
            },
            {
                'product_name': 'iPhone 15 Pro',
                'slug': 'iphone-15-pro',
                'description': 'Apple iPhone 15 Pro with titanium design, A17 Pro chip, 48MP camera system, and USB-C connectivity.',
                'price': 1199.99,
                'discount_price': 1099.99,
                'category_slug': 'electronics',
                'stock_quantity': 50,
                'product_image': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400',
                'rating': 4.7,
                'is_featured': True,
            },
            {
                'product_name': 'Samsung Galaxy S24 Ultra',
                'slug': 'samsung-galaxy-s24-ultra',
                'description': 'Samsung Galaxy S24 Ultra with S Pen, 200MP camera, Snapdragon 8 Gen 3, and titanium frame.',
                'price': 1299.99,
                'discount_price': 1199.99,
                'category_slug': 'electronics',
                'stock_quantity': 35,
                'product_image': 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=400',
                'rating': 4.6,
                'is_featured': True,
            },
            {
                'product_name': 'Sony WH-1000XM5 Headphones',
                'slug': 'sony-wh1000xm5',
                'description': 'Industry-leading noise canceling headphones with exceptional sound quality and 30-hour battery life.',
                'price': 399.99,
                'discount_price': 349.99,
                'category_slug': 'electronics',
                'stock_quantity': 40,
                'product_image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
                'rating': 4.5,
                'is_featured': False,
            },
            {
                'product_name': 'Premium Cotton T-Shirt',
                'slug': 'premium-cotton-tshirt',
                'description': 'Ultra-soft premium cotton t-shirt with a classic fit. Available in multiple colors. Perfect for everyday wear.',
                'price': 29.99,
                'discount_price': 24.99,
                'category_slug': 'clothing',
                'stock_quantity': 200,
                'product_image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
                'rating': 4.3,
                'is_featured': True,
            },
            {
                'product_name': 'Slim Fit Denim Jeans',
                'slug': 'slim-fit-denim-jeans',
                'description': 'Classic slim fit denim jeans with stretch comfort. Dark wash finish with modern styling.',
                'price': 59.99,
                'discount_price': 49.99,
                'category_slug': 'clothing',
                'stock_quantity': 150,
                'product_image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400',
                'rating': 4.2,
                'is_featured': False,
            },
            {
                'product_name': 'Winter Jacket',
                'slug': 'winter-jacket',
                'description': 'Warm and stylish winter jacket with waterproof exterior and fleece lining.',
                'price': 129.99,
                'discount_price': 99.99,
                'category_slug': 'clothing',
                'stock_quantity': 80,
                'product_image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400',
                'rating': 4.4,
                'is_featured': True,
            },
            {
                'product_name': 'Nike Air Max 270',
                'slug': 'nike-air-max-270',
                'description': 'Nike Air Max 270 features the largest heel Air unit yet for a super-soft ride that feels as impossible as it looks.',
                'price': 150.00,
                'discount_price': 129.99,
                'category_slug': 'footwear',
                'stock_quantity': 60,
                'product_image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400',
                'rating': 4.6,
                'is_featured': True,
            },
            {
                'product_name': 'Adidas Ultraboost 22',
                'slug': 'adidas-ultraboost-22',
                'description': 'Premium running shoes with responsive Boost midsole and Primeknit upper for supreme comfort.',
                'price': 190.00,
                'discount_price': 159.99,
                'category_slug': 'footwear',
                'stock_quantity': 45,
                'product_image': 'https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400',
                'rating': 4.5,
                'is_featured': False,
            },
            {
                'product_name': 'Clean Code by Robert C. Martin',
                'slug': 'clean-code-book',
                'description': 'A handbook of agile software craftsmanship. Learn to write clean, maintainable code that works.',
                'price': 39.99,
                'discount_price': 34.99,
                'category_slug': 'books',
                'stock_quantity': 100,
                'product_image': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400',
                'rating': 4.7,
                'is_featured': True,
            },
            {
                'product_name': 'The Pragmatic Programmer',
                'slug': 'pragmatic-programmer',
                'description': 'Your journey to mastery. Classic software development book covering best practices and pragmatic approaches.',
                'price': 49.99,
                'discount_price': 42.99,
                'category_slug': 'books',
                'stock_quantity': 75,
                'product_image': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400',
                'rating': 4.8,
                'is_featured': False,
            },
            {
                'product_name': 'Instant Pot Duo 7-in-1',
                'slug': 'instant-pot-duo',
                'description': 'Multi-use programmable pressure cooker, slow cooker, rice cooker, steamer, sauté, yogurt maker, and warmer.',
                'price': 89.99,
                'discount_price': 69.99,
                'category_slug': 'home-appliances',
                'stock_quantity': 30,
                'product_image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400',
                'rating': 4.4,
                'is_featured': True,
            },
            {
                'product_name': 'Dyson V15 Vacuum',
                'slug': 'dyson-v15-vacuum',
                'description': 'Powerful cordless vacuum with laser dust detection and intelligent suction optimization.',
                'price': 749.99,
                'discount_price': 649.99,
                'category_slug': 'home-appliances',
                'stock_quantity': 20,
                'product_image': 'https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=400',
                'rating': 4.6,
                'is_featured': False,
            },
            {
                'product_name': 'Adjustable Dumbbell Set',
                'slug': 'adjustable-dumbbell-set',
                'description': 'Adjustable dumbbells from 5 to 52.5 lbs. Replace 15 sets of weights. Space-efficient design.',
                'price': 349.99,
                'discount_price': 299.99,
                'category_slug': 'fitness-equipment',
                'stock_quantity': 15,
                'product_image': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400',
                'rating': 4.5,
                'is_featured': True,
            },
            {
                'product_name': 'Yoga Mat Premium',
                'slug': 'yoga-mat-premium',
                'description': 'Extra thick premium yoga mat with alignment lines. Non-slip surface and eco-friendly materials.',
                'price': 49.99,
                'discount_price': 39.99,
                'category_slug': 'fitness-equipment',
                'stock_quantity': 100,
                'product_image': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400',
                'rating': 4.3,
                'is_featured': False,
            },
            {
                'product_name': 'Resistance Bands Set',
                'slug': 'resistance-bands-set',
                'description': 'Set of 5 resistance bands with different tensions. Perfect for home workouts, physical therapy, and stretching.',
                'price': 24.99,
                'discount_price': 19.99,
                'category_slug': 'fitness-equipment',
                'stock_quantity': 200,
                'product_image': 'https://images.unsplash.com/photo-1598632640487-6ea4a4e8b963?w=400',
                'rating': 4.1,
                'is_featured': False,
            },
        ]

        for prod_data in products_data:
            category_slug = prod_data.pop('category_slug')
            category = Category.objects.get(slug=category_slug)
            prod_data['category'] = category
            Product.objects.get_or_create(slug=prod_data['slug'], defaults=prod_data)

        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            UserProfile.objects.get_or_create(user=admin_user)
            self.stdout.write(self.style.WARNING('Superuser created: admin / admin123'))

        # Create sample customer
        if not User.objects.filter(username='customer').exists():
            customer = User.objects.create_user(
                username='customer',
                email='customer@example.com',
                password='customer123',
                first_name='John',
                last_name='Doe'
            )
            UserProfile.objects.get_or_create(
                user=customer,
                defaults={
                    'phone': '+1234567890',
                    'address': '123 Main Street',
                    'city': 'New York',
                    'state': 'NY',
                    'country': 'USA',
                    'zip_code': '10001',
                }
            )
            self.stdout.write(self.style.WARNING('Customer created: customer / customer123'))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))