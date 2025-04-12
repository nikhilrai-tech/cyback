from django.contrib import admin
from .models import Challenge, Question, UserProfile, Participation

class QuestionInline(admin.TabularInline):
    model = Question

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    search_fields = ('name', 'description')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'challenge', 'points', 'created_at')
    list_filter = ('challenge', 'created_at')
    search_fields = ('title', 'description', 'flag')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')
    search_fields = ('user__username',)

class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'joined_at')
    list_filter = ('challenge', 'joined_at')
    search_fields = ('user__username', 'challenge__name')

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Participation, ParticipationAdmin)