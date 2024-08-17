from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path

from .models import Entity, EntityType, Upvote, Application, VisitorApplication


@admin.register(EntityType)
class EntityTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'entity_type', 'location', 'upvotes', 'created_at', 'created_from_application')
    list_filter = ('entity_type', 'created_at', 'created_from_application')
    search_fields = ('name', 'description', 'location')



@admin.register(Upvote)
class UpvoteAdmin(admin.ModelAdmin):
    list_display = ('entity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('entity__name', 'reason')




@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'entity_type', 'status', 'created_at')
    list_filter = ('entity_type', 'status', 'created_at')
    search_fields = ('name', 'description', 'location')
    actions = ['approve_applications', 'reject_applications']

    def approve_applications(self, request, queryset):
        for application in queryset.filter(status='pending'):
            entity = Entity.objects.create(
                name=application.name,
                entity_type=application.entity_type,
                description=application.description,
                location=application.location,
                email=application.email,
                phone=application.phone,
                website=application.website,
                created_from_application=True
            )
            application.status = 'approved'
            application.approved_entity = entity
            application.save()
        self.message_user(request, f"{queryset.filter(status='pending').count()} application(s) approved and added to entities.")
        
    def reject_applications(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f"{updated} application(s) rejected.")
    reject_applications.short_description = "Reject selected applications"




@admin.register(VisitorApplication)
class VisitorApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'entity', 'application_type', 'status', 'created_at')
    list_filter = ('application_type', 'status', 'created_at')
    search_fields = ('name', 'email', 'entity__name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('entity', 'name', 'email', 'phone', 'application_type', 'status')
        }),
        ('Application Details', {
            'fields': ('message', 'cv')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('entity', 'name', 'email', 'phone', 'application_type')
        return self.readonly_fields