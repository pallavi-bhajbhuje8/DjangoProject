from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from courses.models import *


class Command(BaseCommand):
    help = 'Seed the database with premium course data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding LuxLearn data...')

        # Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@luxlearn.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Admin: admin / admin123'))

        # Test user
        student, _ = User.objects.get_or_create(username='student', defaults={
            'email': 'student@luxlearn.com', 'first_name': 'Alexandra', 'last_name': 'Chen'
        })
        student.set_password('student123')
        student.save()
        UserProfile.objects.get_or_create(user=student, defaults={
            'city': 'San Francisco', 'country': 'USA'
        })

        # Instructors
        instr_users = []
        instructors_data = [
            {'username': 'dr_james', 'first_name': 'Dr. James', 'last_name': 'Whitfield',
             'email': 'james@luxlearn.com',
             'bio': 'Former VP of Strategy at McKinsey with 20 years in executive consulting. Harvard MBA, published author, and keynote speaker at Fortune 500 leadership summits worldwide.',
             'headline': 'Executive Strategy & Leadership Expert',
             'avatar_url': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200&h=200&fit=crop&crop=face',
             'expertise': 'Strategy,Leadership,Management,Consulting'},
            {'username': 'sarah_kunst', 'first_name': 'Sarah', 'last_name': 'Kunst',
             'email': 'sarah@luxlearn.com',
             'bio': 'Award-winning UX director with experience at Apple, Airbnb, and Google. Passionate about creating design systems that scale. Speaker at Config and WWDC.',
             'headline': 'UX Director & Design Systems Architect',
             'avatar_url': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200&h=200&fit=crop&crop=face',
             'expertise': 'UX Design,Product Design,Design Systems,Figma'},
            {'username': 'prof_nakamura', 'first_name': 'Prof. Kenji', 'last_name': 'Nakamura',
             'email': 'kenji@luxlearn.com',
             'bio': 'MIT Professor of Computer Science specializing in machine learning and AI ethics. Lead researcher at DeepMind, with 150+ publications.',
             'headline': 'AI & Machine Learning Researcher',
             'avatar_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop&crop=face',
             'expertise': 'AI,Machine Learning,Deep Learning,Python'},
            {'username': 'elena_rich', 'first_name': 'Elena', 'last_name': 'Richardson',
             'email': 'elena@luxlearn.com',
             'bio': 'Former CFO at JP Morgan Private Banking. CFA, MBA from Wharton. Specializes in wealth management education and financial modeling for executives.',
             'headline': 'Finance & Wealth Strategy Advisor',
             'avatar_url': 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=200&h=200&fit=crop&crop=face',
             'expertise': 'Finance,Investing,Wealth Management,Financial Modeling'},
        ]

        instructors = []
        for d in instructors_data:
            u, _ = User.objects.get_or_create(username=d['username'], defaults={
                'first_name': d['first_name'], 'last_name': d['last_name'], 'email': d['email']
            })
            u.set_password('instructor123')
            u.save()
            ip, _ = InstructorProfile.objects.get_or_create(user=u, defaults={
                'bio': d['bio'], 'headline': d['headline'],
                'avatar_url': d['avatar_url'], 'expertise': d['expertise'], 'is_verified': True
            })
            instructors.append(ip)

        # Categories
        cats_data = [
            {'name': 'Leadership & Strategy', 'slug': 'leadership', 'icon': '🎯', 'color': '#8B5D33'},
            {'name': 'Design & Creative', 'slug': 'design', 'icon': '🎨', 'color': '#9C4DCC'},
            {'name': 'Technology & AI', 'slug': 'technology', 'icon': '⚡', 'color': '#2D7DD2'},
            {'name': 'Finance & Business', 'slug': 'finance', 'icon': '💎', 'color': '#1B998B'},
            {'name': 'Marketing & Growth', 'slug': 'marketing', 'icon': '📈', 'color': '#E85D04'},
            {'name': 'Personal Development', 'slug': 'personal-dev', 'icon': '🧠', 'color': '#6A4C93'},
        ]
        cats = {}
        for i, c in enumerate(cats_data):
            cat, _ = Category.objects.update_or_create(slug=c['slug'], defaults={**c, 'display_order': i})
            cats[c['slug']] = cat

        # Courses
        courses_data = [
            {
                'title': 'Executive Leadership Masterclass',
                'slug': 'executive-leadership-masterclass',
                'subtitle': 'Transform your leadership presence and drive organizational excellence',
                'description': 'A comprehensive program designed for senior leaders and aspiring executives. This masterclass covers strategic thinking, organizational transformation, stakeholder management, and the art of executive presence. Drawing from two decades of consulting with Fortune 500 companies, Dr. Whitfield delivers actionable frameworks for modern leadership challenges.',
                'category': cats['leadership'],
                'instructor': instructors[0],
                'level': 'advanced',
                'price': 12999,
                'compare_price': 19999,
                'image': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=500&fit=crop',
                'duration_hours': 24.5,
                'is_featured': True,
                'is_bestseller': True,
                'what_you_learn': 'Develop executive presence and commanding communication\nMaster strategic decision-making frameworks\nBuild high-performing leadership teams\nNavigate organizational politics with integrity\nDrive transformation in complex environments\nCreate lasting organizational culture change',
                'requirements': 'Minimum 5 years management experience\nActive leadership role preferred\nCommitment to 3-4 hours per week',
                'tags': 'leadership,executive,strategy,management,C-suite',
                'modules': [
                    {'title': 'The Executive Mindset', 'lessons': [
                        {'title': 'Introduction to Executive Leadership', 'type': 'video', 'duration': 18, 'free': True},
                        {'title': 'The Strategic Leader Framework', 'type': 'video', 'duration': 25},
                        {'title': 'Self-Assessment: Your Leadership DNA', 'type': 'text', 'duration': 15},
                    ]},
                    {'title': 'Strategic Decision Making', 'lessons': [
                        {'title': 'Decision Frameworks for Uncertainty', 'type': 'video', 'duration': 30},
                        {'title': 'Case Study: Netflix Transformation', 'type': 'text', 'duration': 20},
                        {'title': 'Strategic Thinking Quiz', 'type': 'quiz', 'duration': 15},
                    ]},
                    {'title': 'Building High-Performance Teams', 'lessons': [
                        {'title': 'Team Architecture & Design', 'type': 'video', 'duration': 28},
                        {'title': 'Psychological Safety in Practice', 'type': 'video', 'duration': 22},
                        {'title': 'Conflict Resolution Mastery', 'type': 'text', 'duration': 18},
                    ]},
                ]
            },
            {
                'title': 'Advanced UX Design Systems',
                'slug': 'advanced-ux-design-systems',
                'subtitle': 'Build scalable design systems used by the world\'s best product teams',
                'description': 'Learn to architect, build, and maintain design systems at scale. From atomic design principles to component libraries, tokens, documentation, and governance — this course gives you the complete toolkit used at companies like Airbnb, Shopify, and Google Material Design.',
                'category': cats['design'],
                'instructor': instructors[1],
                'level': 'intermediate',
                'price': 8999,
                'compare_price': 14999,
                'image': 'https://images.unsplash.com/photo-1561070791-2526d30994b5?w=800&h=500&fit=crop',
                'duration_hours': 18.0,
                'is_featured': True,
                'is_bestseller': True,
                'what_you_learn': 'Architect scalable design systems from scratch\nCreate design tokens and component libraries\nBuild documentation that developers love\nEstablish governance and contribution models\nMaster Figma for design system workflows\nMeasure design system adoption and ROI',
                'requirements': 'Proficiency in Figma or Sketch\nBasic understanding of HTML/CSS\n2+ years design experience recommended',
                'tags': 'design,UX,design-systems,figma,product-design',
                'modules': [
                    {'title': 'Design System Foundations', 'lessons': [
                        {'title': 'What Makes a Great Design System', 'type': 'video', 'duration': 22, 'free': True},
                        {'title': 'Atomic Design Methodology', 'type': 'video', 'duration': 28},
                        {'title': 'Auditing Your Existing UI', 'type': 'text', 'duration': 20},
                    ]},
                    {'title': 'Tokens & Components', 'lessons': [
                        {'title': 'Design Tokens Architecture', 'type': 'video', 'duration': 35},
                        {'title': 'Building Your First Components', 'type': 'video', 'duration': 40},
                        {'title': 'Component API Design', 'type': 'text', 'duration': 25},
                        {'title': 'Tokens & Components Quiz', 'type': 'quiz', 'duration': 12},
                    ]},
                ]
            },
            {
                'title': 'Machine Learning Engineering',
                'slug': 'machine-learning-engineering',
                'subtitle': 'From research papers to production-grade ML systems',
                'description': 'Bridge the gap between ML research and real-world engineering. This rigorous course covers model development, MLOps, deployment strategies, monitoring, and the ethical considerations every ML engineer must understand. Taught by a leading MIT researcher with industry experience at DeepMind.',
                'category': cats['technology'],
                'instructor': instructors[2],
                'level': 'advanced',
                'price': 15999,
                'compare_price': 24999,
                'image': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=500&fit=crop',
                'duration_hours': 32.0,
                'is_featured': True,
                'what_you_learn': 'Build production-ready ML pipelines\nMaster MLOps tools and practices\nDeploy models at scale with confidence\nImplement responsible AI frameworks\nOptimize model performance and inference\nDesign ML system architectures',
                'requirements': 'Strong Python programming skills\nLinear algebra and statistics fundamentals\nBasic ML concepts (supervised/unsupervised learning)',
                'tags': 'ML,AI,deep-learning,python,MLOps,engineering',
                'modules': [
                    {'title': 'ML Engineering Foundations', 'lessons': [
                        {'title': 'The ML Engineering Lifecycle', 'type': 'video', 'duration': 20, 'free': True},
                        {'title': 'Setting Up Your ML Environment', 'type': 'text', 'duration': 30},
                        {'title': 'Data Pipeline Architecture', 'type': 'video', 'duration': 35},
                    ]},
                    {'title': 'Model Development', 'lessons': [
                        {'title': 'Feature Engineering at Scale', 'type': 'video', 'duration': 40},
                        {'title': 'Experiment Tracking with MLflow', 'type': 'video', 'duration': 30},
                        {'title': 'Hyperparameter Optimization', 'type': 'video', 'duration': 28},
                        {'title': 'Model Development Quiz', 'type': 'quiz', 'duration': 15},
                    ]},
                    {'title': 'Deployment & Monitoring', 'lessons': [
                        {'title': 'Containerizing ML Models', 'type': 'video', 'duration': 32},
                        {'title': 'CI/CD for Machine Learning', 'type': 'video', 'duration': 26},
                        {'title': 'Model Monitoring & Drift Detection', 'type': 'text', 'duration': 22},
                    ]},
                ]
            },
            {
                'title': 'Wealth Management Fundamentals',
                'slug': 'wealth-management-fundamentals',
                'subtitle': 'Master the principles used by top private bankers and wealth advisors',
                'description': 'An authoritative course on wealth management, portfolio theory, tax optimization, estate planning, and the psychology of wealth. Elena Richardson brings her experience from JP Morgan Private Banking to deliver institutional-grade financial education.',
                'category': cats['finance'],
                'instructor': instructors[3],
                'level': 'intermediate',
                'price': 9999,
                'compare_price': 15999,
                'image': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=500&fit=crop',
                'duration_hours': 20.0,
                'is_featured': True,
                'is_bestseller': True,
                'what_you_learn': 'Build diversified investment portfolios\nUnderstand tax optimization strategies\nMaster financial modeling in Excel\nLearn estate and succession planning\nAnalyze markets with institutional frameworks\nDevelop a personal wealth strategy',
                'requirements': 'Basic understanding of financial markets\nExcel proficiency recommended\nNo prior finance degree needed',
                'tags': 'finance,investing,wealth,portfolio,financial-modeling',
                'modules': [
                    {'title': 'Foundations of Wealth', 'lessons': [
                        {'title': 'The Psychology of Wealth Building', 'type': 'video', 'duration': 20, 'free': True},
                        {'title': 'Asset Classes Deep Dive', 'type': 'video', 'duration': 35},
                        {'title': 'Risk Assessment Framework', 'type': 'text', 'duration': 18},
                    ]},
                    {'title': 'Portfolio Construction', 'lessons': [
                        {'title': 'Modern Portfolio Theory', 'type': 'video', 'duration': 30},
                        {'title': 'Building Your First Portfolio', 'type': 'video', 'duration': 40},
                        {'title': 'Portfolio Quiz', 'type': 'quiz', 'duration': 12},
                    ]},
                ]
            },
            {
                'title': 'Strategic Brand Building',
                'slug': 'strategic-brand-building',
                'subtitle': 'Create iconic brands that command premium positioning',
                'description': 'Learn the art and science of building enduring brands. From brand strategy and positioning to visual identity and storytelling — this course draws from real case studies of luxury and premium brands worldwide.',
                'category': cats['marketing'],
                'instructor': instructors[0],
                'level': 'intermediate',
                'price': 7499,
                'image': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=500&fit=crop',
                'duration_hours': 14.5,
                'is_featured': False,
                'what_you_learn': 'Define compelling brand positioning\nCraft brand narratives that resonate\nDesign brand architecture for growth\nMeasure brand equity and perception\nBuild brand guidelines and governance\nLaunch brands with maximum impact',
                'requirements': 'Interest in marketing and branding\nNo prior experience required',
                'tags': 'branding,marketing,strategy,storytelling',
                'modules': [
                    {'title': 'Brand Foundations', 'lessons': [
                        {'title': 'What Makes a Brand Iconic', 'type': 'video', 'duration': 18, 'free': True},
                        {'title': 'Brand Positioning Framework', 'type': 'video', 'duration': 25},
                        {'title': 'Competitive Analysis Methods', 'type': 'text', 'duration': 20},
                    ]},
                ]
            },
            {
                'title': 'Mindful Productivity for Leaders',
                'slug': 'mindful-productivity-leaders',
                'subtitle': 'Achieve peak performance without burnout through evidence-based practices',
                'description': 'A science-backed approach to sustainable high performance. Combining neuroscience, mindfulness, and productivity systems, this course helps leaders optimize their energy, focus, and decision-making while maintaining wellbeing.',
                'category': cats['personal-dev'],
                'instructor': instructors[1],
                'level': 'beginner',
                'price': 4999,
                'compare_price': 7999,
                'image': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800&h=500&fit=crop',
                'duration_hours': 10.0,
                'is_featured': True,
                'what_you_learn': 'Design your optimal daily routine\nMaster deep work and flow states\nBuild sustainable energy management\nReduce stress with evidence-based techniques\nImprove decision fatigue resilience\nCreate work-life integration strategies',
                'requirements': 'Open mind and willingness to experiment\nJournal or note-taking app',
                'tags': 'productivity,mindfulness,wellness,leadership,performance',
                'modules': [
                    {'title': 'Understanding Your Brain', 'lessons': [
                        {'title': 'Neuroscience of Productivity', 'type': 'video', 'duration': 22, 'free': True},
                        {'title': 'Your Chronotype Assessment', 'type': 'text', 'duration': 15},
                        {'title': 'Energy Management vs Time Management', 'type': 'video', 'duration': 20},
                    ]},
                    {'title': 'Building Your System', 'lessons': [
                        {'title': 'Designing Your Ideal Day', 'type': 'video', 'duration': 25},
                        {'title': 'Deep Work Protocol', 'type': 'video', 'duration': 30},
                        {'title': 'Mindfulness Quiz', 'type': 'quiz', 'duration': 10},
                    ]},
                ]
            },
            {
                'title': 'Python for Data Engineering',
                'slug': 'python-data-engineering',
                'subtitle': 'Build robust data pipelines and infrastructure with Python',
                'description': 'Master the tools and techniques used by data engineers at top tech companies. From ETL pipelines to data warehousing, streaming systems, and infrastructure as code.',
                'category': cats['technology'],
                'instructor': instructors[2],
                'level': 'intermediate',
                'price': 11499,
                'compare_price': 17999,
                'image': 'https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=800&h=500&fit=crop',
                'duration_hours': 28.0,
                'is_featured': False,
                'is_bestseller': True,
                'what_you_learn': 'Design scalable ETL pipelines\nMaster Apache Airflow and Spark\nBuild data warehouses and lakes\nImplement streaming with Kafka\nDeploy infrastructure as code\nMonitor data quality at scale',
                'requirements': 'Intermediate Python skills\nBasic SQL knowledge\nCommand line familiarity',
                'tags': 'python,data-engineering,ETL,spark,airflow',
                'modules': [
                    {'title': 'Data Engineering Essentials', 'lessons': [
                        {'title': 'The Data Engineering Landscape', 'type': 'video', 'duration': 20, 'free': True},
                        {'title': 'Python for Pipelines', 'type': 'video', 'duration': 35},
                        {'title': 'Data Modeling Patterns', 'type': 'text', 'duration': 25},
                    ]},
                ]
            },
            {
                'title': 'The Art of Negotiation',
                'slug': 'art-of-negotiation',
                'subtitle': 'High-stakes negotiation strategies from a Harvard-trained negotiator',
                'description': 'Master the psychology and tactics of world-class negotiation. Whether closing deals, managing stakeholders, or resolving conflicts — this course equips you with frameworks used in boardrooms and diplomatic tables worldwide.',
                'category': cats['leadership'],
                'instructor': instructors[0],
                'level': 'intermediate',
                'price': 8499,
                'image': 'https://images.unsplash.com/photo-1521791136064-7986c2920216?w=800&h=500&fit=crop',
                'duration_hours': 16.0,
                'is_featured': False,
                'what_you_learn': 'Master principled negotiation techniques\nRead body language and micro-expressions\nPrepare strategically for any negotiation\nHandle difficult negotiators with confidence\nCreate win-win outcomes consistently\nNegotiate salary and executive compensation',
                'requirements': 'No prior negotiation training needed\nWillingness to practice through role-plays',
                'tags': 'negotiation,communication,leadership,psychology',
                'modules': [
                    {'title': 'Negotiation Fundamentals', 'lessons': [
                        {'title': 'The Science of Negotiation', 'type': 'video', 'duration': 20, 'free': True},
                        {'title': 'BATNA and Preparation', 'type': 'video', 'duration': 28},
                        {'title': 'Negotiation Styles Assessment', 'type': 'text', 'duration': 15},
                    ]},
                ]
            },
        ]

        for cd in courses_data:
            modules_data = cd.pop('modules', [])
            course, created = Course.objects.update_or_create(slug=cd['slug'], defaults=cd)

            for mi, md in enumerate(modules_data):
                lessons_data = md.pop('lessons', [])
                module, _ = Module.objects.update_or_create(
                    course=course, title=md['title'],
                    defaults={'order': mi, 'description': md.get('description', '')}
                )
                for li, ld in enumerate(lessons_data):
                    lesson, _ = Lesson.objects.update_or_create(
                        module=module, title=ld['title'],
                        defaults={
                            'slug': slugify(ld['title']),
                            'lesson_type': ld.get('type', 'video'),
                            'duration_minutes': ld.get('duration', 15),
                            'order': li,
                            'is_free': ld.get('free', False),
                            'content': f"<h2>{ld['title']}</h2><p>This is the content for the lesson \"{ld['title']}\". In a production environment, this would contain rich text, embedded videos, code samples, and interactive elements.</p><p>Key takeaways from this lesson include understanding the core concepts, applying practical frameworks, and preparing for the next module.</p>",
                        }
                    )
                    if ld.get('type') == 'quiz':
                        quiz, _ = Quiz.objects.get_or_create(lesson=lesson, defaults={'passing_score': 70})
                        questions = [
                            {'text': f'What is the primary focus of "{module.title}"?',
                             'option_a': 'Theoretical knowledge only',
                             'option_b': 'Practical application and frameworks',
                             'option_c': 'Historical context',
                             'option_d': 'None of the above',
                             'correct_answer': 'B',
                             'explanation': 'This module emphasizes practical frameworks.'},
                            {'text': f'Which approach best describes the methodology taught in this course?',
                             'option_a': 'Trial and error',
                             'option_b': 'Theoretical memorization',
                             'option_c': 'Evidence-based systematic approach',
                             'option_d': 'Intuition-based decision making',
                             'correct_answer': 'C',
                             'explanation': 'We follow evidence-based systematic approaches.'},
                            {'text': f'What is the most important skill covered in "{course.title}"?',
                             'option_a': 'Speed of execution',
                             'option_b': 'Strategic thinking and analysis',
                             'option_c': 'Technical proficiency alone',
                             'option_d': 'Memorizing frameworks',
                             'correct_answer': 'B',
                             'explanation': 'Strategic thinking is the core skill.'},
                        ]
                        for qi, qd in enumerate(questions):
                            QuizQuestion.objects.get_or_create(
                                quiz=quiz, text=qd['text'],
                                defaults={**qd, 'order': qi}
                            )

        # Reviews
        courses = Course.objects.all()
        for course in courses[:5]:
            CourseReview.objects.update_or_create(
                course=course, user=student,
                defaults={
                    'rating': 5, 'title': 'Exceptional quality',
                    'comment': f'"{course.title}" exceeded my expectations. The instructor\'s depth of knowledge and the practical frameworks provided are invaluable. Worth every rupee invested.'
                }
            )

        # Sample enrollment
        first_course = Course.objects.first()
        if first_course:
            enrollment, _ = Enrollment.objects.get_or_create(user=student, course=first_course)
            first_lessons = Lesson.objects.filter(module__course=first_course)[:3]
            for lesson in first_lessons:
                LessonProgress.objects.get_or_create(
                    user=student, lesson=lesson,
                    defaults={'is_completed': True, 'completed_at': timezone.now()}
                )

        # Coupons
        now = timezone.now()
        for code, pct, min_amt in [('LUXLEARN30', 30, 5000), ('WELCOME15', 15, 0), ('PREMIUM20', 20, 8000)]:
            Coupon.objects.update_or_create(code=code, defaults={
                'discount_percent': pct, 'min_amount': min_amt,
                'valid_until': now + timedelta(days=90)
            })

        self.stdout.write(self.style.SUCCESS(
            f'Seeded: {Course.objects.count()} courses, {Category.objects.count()} categories, '
            f'{Lesson.objects.count()} lessons, {InstructorProfile.objects.count()} instructors'
        ))
        self.stdout.write(self.style.SUCCESS('Student login: student / student123'))
        self.stdout.write(self.style.SUCCESS('Coupons: LUXLEARN30, WELCOME15, PREMIUM20'))