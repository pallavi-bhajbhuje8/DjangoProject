from django.contrib import admin
from .models import (
    InstructorProfile, Category, Course, Module, Lesson, Quiz,
    QuizQuestion, Enrollment, LessonProgress, QuizAttempt,
    CourseReview, Payment, Coupon, UserProfile
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'course_count', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'instructor', 'price', 'level', 'is_published', 'is_featured']
    list_filter = ['category', 'level', 'is_published', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'lesson_count']
    inlines = [LessonInline]


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 0


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'passing_score']
    inlines = [QuizQuestionInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'enrolled_at', 'progress_percent']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'user', 'course', 'total', 'status', 'method', 'created_at']
    list_filter = ['status', 'method']


admin.site.register(InstructorProfile)
admin.site.register(Lesson)
admin.site.register(LessonProgress)
admin.site.register(QuizAttempt)
admin.site.register(CourseReview)
admin.site.register(Coupon)
admin.site.register(UserProfile)