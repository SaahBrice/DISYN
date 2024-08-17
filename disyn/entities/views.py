from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Entity, EntityType, Upvote, Application, VisitorApplication
from django.db.models import Q
from django.http import JsonResponse
from .forms import ApplicationForm, UpvoteForm, VisitorApplicationForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required




class EntityDetailView(DetailView):
    model = Entity
    template_name = 'entities/entity_detail.html'
    context_object_name = 'entity'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upvote_form'] = UpvoteForm()
        context['upvotes'] = self.object.entity_upvotes.order_by('-created_at')
        return context
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increment_view_count()
        return response


@require_POST
def upvote_entity(request, pk):
    entity = get_object_or_404(Entity, pk=pk)
    form = UpvoteForm(request.POST)
    
    if form.is_valid():
        ip_address = request.META.get('REMOTE_ADDR')
        name = form.cleaned_data['name'] or 'Anonymous'
        role = form.cleaned_data['role']
        reason = form.cleaned_data['reason']
        
        upvote, created = Upvote.objects.get_or_create(
            entity=entity,
            ip_address=ip_address,
            defaults={'name': name, 'role': role, 'reason': reason}
        )
        
        if created:
            entity.upvotes = Upvote.objects.filter(entity=entity).count()
            entity.save()
            return JsonResponse({'success': True, 'upvotes': entity.upvotes})
        else:
            return JsonResponse({'success': False, 'error': 'You have already upvoted this entity.'})
    
    return JsonResponse({'success': False, 'error': 'Invalid form data.'})



class EntityListView(ListView):
    model = Entity
    template_name = 'entities/entity_list.html'
    context_object_name = 'entities'
    paginate_by = 10

    def get_queryset(self):
        queryset = Entity.objects.annotate(upvote_count=Count('entity_upvotes'))
        search_query = self.request.GET.get('search')
        entity_type = self.request.GET.get('type')

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(location__icontains=search_query)
            )
        
        if entity_type:
            queryset = queryset.filter(entity_type__name=entity_type)

        return queryset.order_by('-upvote_count', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity_types'] = EntityType.objects.all()
        return context

def get_recent_upvotes(request, pk):
    entity = get_object_or_404(Entity, pk=pk)
    recent_upvotes = entity.entity_upvotes.order_by('-created_at')[:5]
    html = render_to_string('entities/recent_upvotes.html', {'upvotes': recent_upvotes})
    return JsonResponse({'html': html})

class ApplicationCreateView(CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'entities/application_form.html'
    success_url = reverse_lazy('application_success')

def application_success(request):
    return render(request, 'entities/application_success.html')

@user_passes_test(lambda u: u.is_superuser)
def analytics_dashboard(request):
    # Total counts
    total_entities = Entity.objects.count()
    total_upvotes = Upvote.objects.count()
    total_applications = VisitorApplication.objects.count()

    # Most upvoted entities
    most_upvoted = Entity.objects.annotate(upvote_count=Count('entity_upvotes')).order_by('-upvote_count')[:5]

    # Most viewed entities
    most_viewed = Entity.objects.order_by('-view_count')[:5]

    # Entity distribution by type
    entity_types = EntityType.objects.annotate(count=Count('entities'))

    # Recent activity
    recent_entities = Entity.objects.order_by('-created_at')[:5]
    recent_upvotes = Upvote.objects.order_by('-created_at')[:5]
    recent_applications = VisitorApplication.objects.order_by('-created_at')[:5]

    # Upvotes over time (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    upvotes_over_time = Upvote.objects.filter(created_at__gte=thirty_days_ago) \
        .extra(select={'date': 'date(created_at)'}) \
        .values('date') \
        .annotate(count=Count('id')) \
        .order_by('date')

    context = {
        'total_entities': total_entities,
        'total_upvotes': total_upvotes,
        'total_applications': total_applications,
        'most_upvoted': most_upvoted,
        'most_viewed': most_viewed,
        'entity_types': entity_types,
        'recent_entities': recent_entities,
        'recent_upvotes': recent_upvotes,
        'recent_applications': recent_applications,
        'upvotes_over_time': list(upvotes_over_time),
    }

    return render(request, 'entities/analytics_dashboard.html', context)




class ApplicationListView(ListView):
    model = Application
    template_name = 'entities/application_list.html'
    context_object_name = 'applications'
    paginate_by = 20

    def get_queryset(self):
        return Application.objects.all().order_by('-created_at')


class ApplicationDetailView(DetailView):
    model = Application
    template_name = 'entities/application_detail.html'
    context_object_name = 'application'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        action = request.POST.get('action')
        
        if action == 'approve':
            self.object.status = 'approved'
            Entity.objects.create(
                name=self.object.name,
                entity_type=self.object.entity_type,
                description=self.object.description,
                location=self.object.location,
                email=self.object.email,
                phone=self.object.phone,
                website=self.object.website
            )
        elif action == 'reject':
            self.object.status = 'rejected'
        
        self.object.save()
        return redirect(reverse('application_list'))
    



def submit_visitor_application(request, pk):
    entity = get_object_or_404(Entity, pk=pk)
    if request.method == 'POST':
        form = VisitorApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.entity = entity
            application.save()
            messages.success(request, 'Your application has been submitted successfully.')
            return redirect('entity_detail', pk=pk)
    else:
        form = VisitorApplicationForm()
    
    return render(request, 'entities/submit_visitor_application.html', {'form': form, 'entity': entity})



@staff_member_required
def entity_visitor_applications(request, pk):
    entity = get_object_or_404(Entity, pk=pk)
    applications = entity.visitor_applications.all().order_by('-created_at')
    return render(request, 'entities/entity_visitor_applications.html', {'entity': entity, 'applications': applications})




def landing_page(request):
    return render(request, 'entities/landing_page.html')



@staff_member_required
def visitor_applications_list(request):
    applications = VisitorApplication.objects.all().order_by('-created_at')
    return render(request, 'entities/visitor_applications_list.html', {'applications': applications})

@staff_member_required
def visitor_application_detail(request, pk):
    application = get_object_or_404(VisitorApplication, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action in ['approve', 'reject']:
            application.status = action
            application.save()
            messages.success(request, f'Application {action}d successfully.')
            return redirect('visitor_applications_list')
    return render(request, 'entities/visitor_application_detail.html', {'application': application})