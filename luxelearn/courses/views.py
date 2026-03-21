import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg, Count, Sum
from django.utils import timezone
from .models import (
    Category, Course, Module, Lesson, Quiz, QuizQuestion,
    Enrollment, LessonProgress, QuizAttempt, CourseReview,
    Payment, Coupon, UserProfile, InstructorProfile
)


def home(request):
    featured = Course.objects.filter(is_published=True, is_featured=True)[:6]
    bestsellers = Course.objects.filter(is_published=True, is_bestseller=True)[:4]
    latest = Course.objects.filter(is_published=True).order_by('-created_at')[:8]
    categories = Category.objects.filter(is_active=True)
    total_students = Enrollment.objects.count()
    total_courses = Course.objects.filter(is_published=True).count()

    context = {
        'featured': featured,
        'bestsellers': bestsellers,
        'latest': latest,
        'categories': categories,
        'total_students': total_students,
        'total_courses': total_courses,
    }
    return render(request, 'courses/home.html', context)


def catalog(request):
    courses = Course.objects.filter(is_published=True)
    categories = Category.objects.filter(is_active=True)

    q = request.GET.get('q', '')
    if q:
        courses = courses.filter(
            Q(title__icontains=q) | Q(description__icontains=q) | Q(tags__icontains=q)
        )

    cat_slug = request.GET.get('category', '')
    if cat_slug:
        courses = courses.filter(category__slug=cat_slug)

    level = request.GET.get('level', '')
    if level:
        courses = courses.filter(level=level)

    price_range = request.GET.get('price', '')
    if price_range == 'free':
        courses = courses.filter(price=0)
    elif price_range == 'under1000':
        courses = courses.filter(price__gt=0, price__lte=1000)
    elif price_range == 'under5000':
        courses = courses.filter(price__gt=1000, price__lte=5000)
    elif price_range == 'premium':
        courses = courses.filter(price__gt=5000)

    sort = request.GET.get('sort', 'newest')
    if sort == 'price_low':
        courses = courses.order_by('price')
    elif sort == 'price_high':
        courses = courses.order_by('-price')
    elif sort == 'popular':
        courses = courses.annotate(enroll_count=Count('enrollments')).order_by('-enroll_count')
    elif sort == 'rated':
        courses = courses.annotate(avg_r=Avg('reviews__rating')).order_by('-avg_r')
    else:
        courses = courses.order_by('-created_at')

    active_cat = Category.objects.filter(slug=cat_slug).first() if cat_slug else None

    context = {
        'courses': courses,
        'categories': categories,
        'query': q,
        'active_category': active_cat,
        'current_level': level,
        'current_price': price_range,
        'current_sort': sort,
    }
    return render(request, 'courses/catalog.html', context)


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    modules = course.modules.prefetch_related('lessons').all()
    reviews = course.reviews.select_related('user').all()[:10]
    related = Course.objects.filter(
        category=course.category, is_published=True
    ).exclude(id=course.id)[:4]

    is_enrolled = False
    enrollment = None
    user_review = None
    lesson_progress_ids = []

    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        is_enrolled = enrollment is not None
        user_review = CourseReview.objects.filter(course=course, user=request.user).first()
        lesson_progress_ids = list(
            LessonProgress.objects.filter(
                user=request.user, lesson__module__course=course, is_completed=True
            ).values_list('lesson_id', flat=True)
        )

    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        title = request.POST.get('title', '')
        if rating and is_enrolled:
            CourseReview.objects.update_or_create(
                course=course, user=request.user,
                defaults={'rating': int(rating), 'comment': comment, 'title': title}
            )
            messages.success(request, 'Review submitted!')
            return redirect('course_detail', slug=slug)

    context = {
        'course': course,
        'modules': modules,
        'reviews': reviews,
        'related': related,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'user_review': user_review,
        'lesson_progress_ids': lesson_progress_ids,
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
def lesson_view(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)

    lesson = None
    for module in course.modules.prefetch_related('lessons').all():
        for l in module.lessons.all():
            if l.slug == lesson_slug:
                lesson = l
                break
        if lesson:
            break

    if not lesson:
        messages.error(request, 'Lesson not found.')
        return redirect('course_detail', slug=course_slug)

    # Build ordered lesson list for prev/next
    all_lessons = []
    for module in course.modules.prefetch_related('lessons').all():
        for l in module.lessons.all():
            all_lessons.append(l)

    current_idx = next((i for i, l in enumerate(all_lessons) if l.id == lesson.id), 0)
    prev_lesson = all_lessons[current_idx - 1] if current_idx > 0 else None
    next_lesson = all_lessons[current_idx + 1] if current_idx < len(all_lessons) - 1 else None

    progress, _ = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'complete':
            progress.is_completed = True
            progress.completed_at = timezone.now()
            progress.save()
            messages.success(request, f'"{lesson.title}" marked complete!')
            if next_lesson:
                return redirect('lesson', course_slug=course_slug, lesson_slug=next_lesson.slug)
            return redirect('course_detail', slug=course_slug)
        elif action == 'save_notes':
            progress.notes = request.POST.get('notes', '')
            progress.save()
            messages.success(request, 'Notes saved!')
            return redirect('lesson', course_slug=course_slug, lesson_slug=lesson_slug)

    completed_ids = list(
        LessonProgress.objects.filter(
            user=request.user, lesson__module__course=course, is_completed=True
        ).values_list('lesson_id', flat=True)
    )

    context = {
        'course': course,
        'lesson': lesson,
        'enrollment': enrollment,
        'progress': progress,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'all_lessons': all_lessons,
        'completed_ids': completed_ids,
        'lesson_number': current_idx + 1,
        'total_lessons': len(all_lessons),
    }
    return render(request, 'courses/lesson.html', context)


@login_required
def quiz_view(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)

    lesson = None
    for module in course.modules.prefetch_related('lessons').all():
        for l in module.lessons.all():
            if l.slug == lesson_slug:
                lesson = l
                break
        if lesson:
            break

    if not lesson or not hasattr(lesson, 'quiz'):
        messages.error(request, 'Quiz not found.')
        return redirect('course_detail', slug=course_slug)

    quiz = lesson.quiz
    questions = quiz.questions.all()
    last_attempt = QuizAttempt.objects.filter(user=request.user, quiz=quiz).first()

    if request.method == 'POST':
        answers = {}
        score = 0
        for q in questions:
            user_answer = request.POST.get(f'q_{q.id}', '')
            answers[str(q.id)] = user_answer
            if user_answer.upper() == q.correct_answer.upper():
                score += 1

        total = questions.count()
        percentage = int((score / total) * 100) if total > 0 else 0
        passed = percentage >= quiz.passing_score

        attempt = QuizAttempt.objects.create(
            user=request.user, quiz=quiz,
            score=score, total_questions=total,
            passed=passed, answers=answers
        )

        if passed:
            progress, _ = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
            progress.is_completed = True
            progress.completed_at = timezone.now()
            progress.save()
            messages.success(request, f'Congratulations! You scored {percentage}% and passed!')
        else:
            messages.warning(request, f'You scored {percentage}%. You need {quiz.passing_score}% to pass.')

        return redirect('quiz', course_slug=course_slug, lesson_slug=lesson_slug)

    context = {
        'course': course,
        'lesson': lesson,
        'quiz': quiz,
        'questions': questions,
        'last_attempt': last_attempt,
    }
    return render(request, 'courses/quiz.html', context)


@login_required
def checkout(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)

    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.info(request, 'You are already enrolled in this course.')
        return redirect('course_detail', slug=slug)

    tax_rate = 0.18
    tax = round(float(course.price) * tax_rate, 2)
    total = round(float(course.price) + tax, 2)
    discount = 0

    if request.method == 'POST':
        method = request.POST.get('payment_method', 'card')
        coupon_code = request.POST.get('coupon_code', '').strip().upper()

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if coupon.is_valid and float(course.price) >= float(coupon.min_amount):
                    discount = round(float(course.price) * coupon.discount_percent / 100, 2)
                    total = round(float(course.price) - discount + tax, 2)
                    coupon.used_count += 1
                    coupon.save()
            except Coupon.DoesNotExist:
                pass

        payment = Payment.objects.create(
            user=request.user, course=course,
            amount=course.price, discount=discount,
            tax=tax, total=total,
            status='completed', method=method,
            coupon_code=coupon_code
        )

        Enrollment.objects.create(user=request.user, course=course)
        messages.success(request, f'Successfully enrolled in "{course.title}"!')
        return redirect('receipt', payment_id=payment.payment_id)

    context = {
        'course': course,
        'tax': tax,
        'total': total,
    }
    return render(request, 'courses/checkout.html', context)


@login_required
def receipt_view(request, payment_id):
    payment = get_object_or_404(Payment, payment_id=payment_id, user=request.user)
    return render(request, 'courses/receipt.html', {'payment': payment})


@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    total_enrolled = enrollments.count()
    completed_count = sum(1 for e in enrollments if e.progress_percent == 100)
    in_progress = total_enrolled - completed_count
    total_spent = Payment.objects.filter(
        user=request.user, status='completed'
    ).aggregate(Sum('total'))['total__sum'] or 0
    recent_payments = Payment.objects.filter(user=request.user, status='completed')[:5]

    context = {
        'enrollments': enrollments,
        'total_enrolled': total_enrolled,
        'completed_count': completed_count,
        'in_progress': in_progress,
        'total_spent': total_spent,
        'recent_payments': recent_payments,
    }
    return render(request, 'courses/dashboard.html', context)


@login_required
def instructor_dashboard(request):
    try:
        instructor = request.user.instructor_profile
    except InstructorProfile.DoesNotExist:
        messages.error(request, 'You are not registered as an instructor.')
        return redirect('home')

    courses = instructor.courses.all()
    total_students = sum(c.enrollment_count for c in courses)
    total_revenue = Payment.objects.filter(
        course__instructor=instructor, status='completed'
    ).aggregate(Sum('total'))['total__sum'] or 0
    recent_enrollments = Enrollment.objects.filter(
        course__instructor=instructor
    ).select_related('user', 'course').order_by('-enrolled_at')[:10]
    avg_rating = instructor.average_rating

    context = {
        'instructor': instructor,
        'courses': courses,
        'total_students': total_students,
        'total_revenue': total_revenue,
        'recent_enrollments': recent_enrollments,
        'avg_rating': avg_rating,
    }
    return render(request, 'courses/instructor.html', context)


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        profile.phone = request.POST.get('phone', '')
        profile.city = request.POST.get('city', '')
        profile.country = request.POST.get('country', '')
        profile.bio = request.POST.get('bio', '')
        profile.linkedin = request.POST.get('linkedin', '')
        profile.save()
        messages.success(request, 'Profile updated!')
        return redirect('profile')

    context = {'profile': profile}
    return render(request, 'courses/profile.html', context)


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(request.GET.get('next', 'home'))
        messages.error(request, 'Invalid credentials.')
    return render(request, 'courses/login.html')


def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password,
                first_name=first_name, last_name=last_name
            )
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Welcome to LuxLearn!')
            return redirect('home')
    return render(request, 'courses/register.html')


def user_logout(request):
    logout(request)
    messages.info(request, 'Signed out.')
    return redirect('home')