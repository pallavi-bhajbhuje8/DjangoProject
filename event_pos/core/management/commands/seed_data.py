from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from core.models import Category, Product, Coupon, Review


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superuser created: admin / admin123'))

        # Create test user
        user, _ = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Alex',
                'last_name': 'Morgan',
            }
        )
        user.set_password('test1234')
        user.save()

        # Categories
        categories_data = [
            {
                'name': 'Appetizers',
                'slug': 'appetizers',
                'icon': '🍤',
                'description': 'Start your event with delicious bites',
                'image': 'https://images.unsplash.com/photo-1541014741259-de529411b96a?w=400&h=300&fit=crop',
            },
            {
                'name': 'Main Course',
                'slug': 'main-course',
                'icon': '🥩',
                'description': 'Hearty entrees for the main event',
                'image': 'https://images.unsplash.com/photo-1544025162-d76694265947?w=400&h=300&fit=crop',
            },
            {
                'name': 'Desserts',
                'slug': 'desserts',
                'icon': '🍰',
                'description': 'Sweet endings to memorable occasions',
                'image': 'https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=300&fit=crop',
            },
            {
                'name': 'Beverages',
                'slug': 'beverages',
                'icon': '🍹',
                'description': 'Refreshing drinks & cocktails',
                'image': 'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=400&h=300&fit=crop',
            },
            {
                'name': 'Salads',
                'slug': 'salads',
                'icon': '🥗',
                'description': 'Fresh & healthy garden selections',
                'image': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&h=300&fit=crop',
            },
            {
                'name': 'Seafood',
                'slug': 'seafood',
                'icon': '🦞',
                'description': 'Premium ocean-to-table selections',
                'image': 'https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=400&h=300&fit=crop',
            },
        ]

        categories = {}
        for i, cat_data in enumerate(categories_data):
            cat, _ = Category.objects.update_or_create(
                slug=cat_data['slug'],
                defaults={**cat_data, 'display_order': i}
            )
            categories[cat_data['slug']] = cat

        # Products
        products_data = [
            # Appetizers
            {
                'name': 'Truffle Arancini',
                'slug': 'truffle-arancini',
                'category': categories['appetizers'],
                'price': 320,
                'compare_price': 399,
                'description': 'Crispy risotto balls infused with black truffle, filled with mozzarella and served with a saffron aioli. Each piece is hand-rolled and golden-fried to perfection.',
                'short_description': 'Crispy truffle risotto balls with saffron aioli',
                'image': 'https://images.unsplash.com/photo-1541014741259-de529411b96a?w=600&h=600&fit=crop',
                'image_2': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600&h=600&fit=crop',
                'brand': 'Chef\'s Special',
                'stock': 50,
                'is_featured': True,
                'is_new': True,
                'tags': 'truffle,italian,crispy,appetizer',
                'calories': '280 cal',
                'prep_time': '15 min',
                'serves': '2-3',
            },
            {
                'name': 'Spicy Tuna Tartare',
                'slug': 'spicy-tuna-tartare',
                'category': categories['appetizers'],
                'price': 480,
                'compare_price': 550,
                'description': 'Fresh ahi tuna diced and tossed with sriracha mayo, sesame oil, and crispy wonton chips. Garnished with microgreens and tobiko.',
                'short_description': 'Fresh ahi tuna with sriracha mayo & wonton chips',
                'image': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=600&h=600&fit=crop',
                'brand': 'Ocean Fresh',
                'stock': 30,
                'is_featured': True,
                'tags': 'tuna,spicy,japanese,raw',
                'calories': '190 cal',
                'prep_time': '10 min',
                'serves': '2',
            },
            {
                'name': 'Burrata & Prosciutto',
                'slug': 'burrata-prosciutto',
                'category': categories['appetizers'],
                'price': 420,
                'description': 'Creamy burrata cheese draped with aged prosciutto di Parma, heirloom tomatoes, and a balsamic reduction drizzle on artisan crostini.',
                'short_description': 'Creamy burrata with aged prosciutto & balsamic',
                'image': 'https://images.unsplash.com/photo-1608897013039-887f21d8c804?w=600&h=600&fit=crop',
                'brand': 'Artisan Table',
                'stock': 40,
                'is_featured': False,
                'is_new': True,
                'tags': 'italian,cheese,prosciutto',
                'calories': '340 cal',
                'prep_time': '8 min',
                'serves': '2-4',
            },
            # Main Course
            {
                'name': 'Wagyu Beef Ribeye',
                'slug': 'wagyu-beef-ribeye',
                'category': categories['main-course'],
                'price': 1850,
                'compare_price': 2200,
                'description': 'A5 Wagyu ribeye, dry-aged for 28 days, seared to perfection and served with truffle mashed potatoes, roasted seasonal vegetables, and a red wine reduction.',
                'short_description': 'A5 Wagyu 28-day dry-aged with truffle mash',
                'image': 'https://images.unsplash.com/photo-1544025162-d76694265947?w=600&h=600&fit=crop',
                'image_2': 'https://images.unsplash.com/photo-1558030006-450675393462?w=600&h=600&fit=crop',
                'brand': 'Prime Cuts',
                'stock': 20,
                'is_featured': True,
                'tags': 'wagyu,steak,premium,beef',
                'calories': '680 cal',
                'prep_time': '35 min',
                'serves': '1',
            },
            {
                'name': 'Herb-Crusted Lamb Rack',
                'slug': 'herb-crusted-lamb-rack',
                'category': categories['main-course'],
                'price': 1450,
                'description': 'New Zealand lamb rack crusted with fresh rosemary, thyme, and Dijon mustard. Served with roasted fingerling potatoes and mint chimichurri.',
                'short_description': 'NZ lamb rack with rosemary crust & mint chimichurri',
                'image': 'https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=600&h=600&fit=crop',
                'brand': 'Prime Cuts',
                'stock': 25,
                'is_featured': True,
                'is_new': True,
                'tags': 'lamb,herb,premium',
                'calories': '620 cal',
                'prep_time': '40 min',
                'serves': '2',
            },
            {
                'name': 'Pan-Seared Duck Breast',
                'slug': 'pan-seared-duck-breast',
                'category': categories['main-course'],
                'price': 980,
                'compare_price': 1150,
                'description': 'Perfectly rendered duck breast served with a cherry port wine sauce, pomme purée, and wilted baby spinach. A classic French technique.',
                'short_description': 'Duck breast with cherry port sauce & pomme purée',
                'image': 'https://images.unsplash.com/photo-1432139509613-5c4255a78e00?w=600&h=600&fit=crop',
                'brand': 'French Table',
                'stock': 35,
                'is_featured': False,
                'tags': 'duck,french,elegant',
                'calories': '520 cal',
                'prep_time': '30 min',
                'serves': '1',
            },
            {
                'name': 'Lobster Thermidor',
                'slug': 'lobster-thermidor',
                'category': categories['seafood'],
                'price': 2200,
                'compare_price': 2600,
                'description': 'Whole Maine lobster split and filled with a rich cognac cream sauce, topped with Gruyère cheese, and broiled until golden. Served with drawn butter.',
                'short_description': 'Maine lobster with cognac cream & Gruyère',
                'image': 'https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=600&h=600&fit=crop',
                'brand': 'Ocean Fresh',
                'stock': 15,
                'is_featured': True,
                'tags': 'lobster,premium,seafood,french',
                'calories': '780 cal',
                'prep_time': '45 min',
                'serves': '1-2',
            },
            {
                'name': 'Grilled Mediterranean Seabass',
                'slug': 'grilled-mediterranean-seabass',
                'category': categories['seafood'],
                'price': 890,
                'description': 'Whole Mediterranean seabass grilled with lemon, capers, and fresh herbs. Served with sautéed vegetables and a lemon beurre blanc.',
                'short_description': 'Whole seabass with lemon, capers & beurre blanc',
                'image': 'https://images.unsplash.com/photo-1580476262798-bddd9f4b7369?w=600&h=600&fit=crop',
                'brand': 'Ocean Fresh',
                'stock': 28,
                'is_new': True,
                'tags': 'fish,mediterranean,healthy',
                'calories': '380 cal',
                'prep_time': '25 min',
                'serves': '1-2',
            },
            # Desserts
            {
                'name': 'Dark Chocolate Fondant',
                'slug': 'dark-chocolate-fondant',
                'category': categories['desserts'],
                'price': 380,
                'description': 'Valrhona 70% dark chocolate fondant with a molten center, served with vanilla bean ice cream and a dusting of gold leaf. Pure indulgence.',
                'short_description': 'Molten Valrhona chocolate with vanilla ice cream',
                'image': 'https://images.unsplash.com/photo-1551024506-0bccd828d307?w=600&h=600&fit=crop',
                'image_2': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600&h=600&fit=crop',
                'brand': 'Pâtisserie',
                'stock': 40,
                'is_featured': True,
                'tags': 'chocolate,dessert,french',
                'calories': '450 cal',
                'prep_time': '20 min',
                'serves': '1',
            },
            {
                'name': 'Crème Brûlée Trio',
                'slug': 'creme-brulee-trio',
                'category': categories['desserts'],
                'price': 350,
                'description': 'A trio of classic crème brûlées: Madagascar vanilla, Earl Grey lavender, and passion fruit. Each topped with a caramelized sugar crust.',
                'short_description': 'Three flavors: vanilla, lavender & passion fruit',
                'image': 'https://images.unsplash.com/photo-1470324161839-ce2bb6fa6bc3?w=600&h=600&fit=crop',
                'brand': 'Pâtisserie',
                'stock': 45,
                'is_new': True,
                'tags': 'french,custard,dessert',
                'calories': '320 cal',
                'prep_time': '4 hrs',
                'serves': '1',
            },
            {
                'name': 'Pistachio Rose Tart',
                'slug': 'pistachio-rose-tart',
                'category': categories['desserts'],
                'price': 420,
                'description': 'Delicate tart with pistachio frangipane, rose cream, and fresh raspberries on a buttery sablé crust. Finished with candied rose petals.',
                'short_description': 'Pistachio frangipane tart with rose cream',
                'image': 'https://images.unsplash.com/photo-1519915028121-7d3463d20b13?w=600&h=600&fit=crop',
                'brand': 'Pâtisserie',
                'stock': 30,
                'is_featured': True,
                'tags': 'tart,pistachio,rose,elegant',
                'calories': '390 cal',
                'prep_time': '2 hrs',
                'serves': '1-2',
            },
            # Beverages
            {
                'name': 'Espresso Martini',
                'slug': 'espresso-martini',
                'category': categories['beverages'],
                'price': 450,
                'description': 'Freshly brewed espresso shaken with premium vodka, Kahlúa, and a touch of vanilla syrup. Served ice cold with coffee beans.',
                'short_description': 'Vodka, espresso & Kahlúa shaken ice cold',
                'image': 'https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=600&h=600&fit=crop',
                'brand': 'Bar Luxe',
                'stock': 100,
                'is_featured': True,
                'tags': 'cocktail,coffee,vodka',
                'calories': '180 cal',
                'prep_time': '5 min',
                'serves': '1',
            },
            {
                'name': 'Mango Passionfruit Cooler',
                'slug': 'mango-passionfruit-cooler',
                'category': categories['beverages'],
                'price': 280,
                'description': 'A refreshing blend of Alphonso mango, passion fruit, sparkling water, and a hint of mint. Non-alcoholic and perfect for summer events.',
                'short_description': 'Alphonso mango & passion fruit sparkling cooler',
                'image': 'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=600&h=600&fit=crop',
                'brand': 'Fresh Press',
                'stock': 80,
                'is_new': True,
                'tags': 'mocktail,fruit,refreshing,non-alcoholic',
                'calories': '120 cal',
                'prep_time': '3 min',
                'serves': '1',
            },
            # Salads
            {
                'name': 'Caesar Royale',
                'slug': 'caesar-royale',
                'category': categories['salads'],
                'price': 380,
                'compare_price': 450,
                'description': 'Romaine hearts, house-made Caesar dressing, shaved Parmigiano-Reggiano, anchovy crumble, and sourdough croutons. Topped with grilled prawns.',
                'short_description': 'Classic Caesar with grilled prawns & Parmigiano',
                'image': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&h=600&fit=crop',
                'brand': 'Garden Table',
                'stock': 50,
                'is_featured': True,
                'tags': 'salad,healthy,prawns,classic',
                'calories': '290 cal',
                'prep_time': '12 min',
                'serves': '1-2',
            },
            {
                'name': 'Burrata & Peach Salad',
                'slug': 'burrata-peach-salad',
                'category': categories['salads'],
                'price': 420,
                'description': 'Fresh burrata surrounded by grilled peaches, arugula, toasted walnuts, and drizzled with a honey balsamic vinaigrette.',
                'short_description': 'Grilled peach, burrata & honey balsamic',
                'image': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600&h=600&fit=crop',
                'brand': 'Garden Table',
                'stock': 35,
                'is_new': True,
                'tags': 'salad,burrata,peach,summer',
                'calories': '310 cal',
                'prep_time': '10 min',
                'serves': '1-2',
            },
        ]

        for prod_data in products_data:
            Product.objects.update_or_create(
                slug=prod_data['slug'],
                defaults=prod_data
            )

        # Coupons
        now = timezone.now()
        coupons_data = [
            {
                'code': 'WELCOME20',
                'discount_type': 'percentage',
                'discount_value': 20,
                'min_order_amount': 500,
                'valid_from': now,
                'valid_until': now + timedelta(days=90),
            },
            {
                'code': 'FLAT200',
                'discount_type': 'fixed',
                'discount_value': 200,
                'min_order_amount': 1000,
                'valid_from': now,
                'valid_until': now + timedelta(days=60),
            },
            {
                'code': 'EVENT10',
                'discount_type': 'percentage',
                'discount_value': 10,
                'min_order_amount': 300,
                'valid_from': now,
                'valid_until': now + timedelta(days=120),
            },
        ]

        for coupon_data in coupons_data:
            Coupon.objects.update_or_create(
                code=coupon_data['code'],
                defaults=coupon_data
            )

        # Sample reviews
        products = Product.objects.all()
        for product in products[:8]:
            Review.objects.update_or_create(
                product=product,
                user=user,
                defaults={
                    'rating': 5 if product.is_featured else 4,
                    'title': f'Amazing {product.name}!',
                    'comment': f'The {product.name} exceeded all expectations. Presentation was stunning and the flavors were incredible. Perfect for our event catering.',
                }
            )

        self.stdout.write(self.style.SUCCESS(
            f'Seeded: {Category.objects.count()} categories, '
            f'{Product.objects.count()} products, '
            f'{Coupon.objects.count()} coupons, '
            f'{Review.objects.count()} reviews'
        ))