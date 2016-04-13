import datetime
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse 
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Q
from usernotes.models import Usernote, Category
from usernotes.forms import UsernoteForm
    
USERNOTES_PER_PAGE = 5

def category(request, category_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    
    category = Category.objects.filter(id = category_id)
    notes = Usernote.objects.filter(category_id = category_id)
    return render_to_response('category.html', {
        'notes': notes, 
        'category': category
    })


def add_note(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UsernoteForm(request.POST)
        if form.is_valid():
            # TODO: save new Usernote here ...
            form.save(request=request)
            
            return HttpResponseRedirect('/note/')

    else:
        form = UsernoteForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('note_add.html', 
        args, 
        context_instance = RequestContext(request)
    )
    
def edit_note(request, note_id):   
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
     
    usernote = get_object_or_404(Usernote, id = note_id) # instance
    if usernote.user_id != request.user.id:
        raise Http404

    if request.method == 'POST':
        if 'delete' in request.POST:
            usernote.delete()
            return HttpResponseRedirect('/note/')
        else: # edit
            # create a form instance and populate it with data from the request:
            form = UsernoteForm(request.POST, usernote=usernote)
            if form.is_valid():
                # TODO: save new Usernote here ...
                form.save()
                return HttpResponseRedirect('/note/')

    else: # before edit
        if usernote.user_id != request.user.id:
            raise Http404
        form = UsernoteForm(usernote.__dict__)
    
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['note_id'] = note_id
    return render_to_response('note_edit.html', 
        args,
        context_instance = RequestContext(request)
    )
    

# ------------------
@csrf_exempt
def notes_list(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    
    # False if collection has some more elements, which not shown yet.
    end_of_collection = False
    
    date_format_request = '%d/%m/%Y'
    date_format_db = '%Y-%m-%d'
    date_from = request.GET.get('date_from')
    if date_from:
        date_1 = datetime.datetime.strptime(date_from, date_format_request).strftime(date_format_db)
    else:
        date_1 = '1970-01-01'    
    date_to = request.GET.get('date_to')
    if date_to:
        date_2 = datetime.datetime.strptime(date_to, date_format_request).strftime(date_format_db)
    else:
        date_2 = '2100-01-01'
    
    title = request.GET.get('title')    
    category_id = request.GET.get('category')
    favorite_only = request.GET.get('favorite')
    sort = request.GET.get('sort')
    order_by = '-created'
    if sort == 'date_desc':
        order_by = '-created'
    elif sort == 'date_asc':
        order_by = 'created'
    elif sort == 'category':
        order_by = 'category'
    elif sort == 'favorite':
        order_by = '-is_favorite'
    page = request.GET.get('page')
    if not page:
        page = 1
    else:
        page = int(page)
    offset = (page - 1) * USERNOTES_PER_PAGE
    to_offset = offset + USERNOTES_PER_PAGE;
    
    filters = {}
    filters['user_id'] = request.user.id
    if category_id:
        filters['category_id'] = category_id
    if favorite_only:
        filters['is_favorite'] = 1
    if title:
        filters['title__icontains'] = title
    filters['created__range'] = [date_1, date_2]
    usernotes = Usernote.objects.filter(**filters) \
            .select_related('category') \
            .order_by(order_by)[offset:to_offset] # fixxx
    count_total = Usernote.objects.filter(**filters).count();
    if count_total <= to_offset:
        end_of_collection = True    
    args = {}
    args['usernotes'] = usernotes    
        
    if request.is_ajax():
        html = render_to_string('notes_items.html', 
            args, 
            context_instance = RequestContext(request)
        )
        response = HttpResponse(html)
        if end_of_collection:
            response['X-End-Of-Collection'] = 1        
        return response
    else:
        categories = Category.objects.order_by('sort')
        args['categories'] = categories
        args['need_load_more_button'] = not end_of_collection
        return render_to_response('notes.html',
            args,
            context_instance = RequestContext(request)
        )
        


# -------------------------
def note_view(request, note_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    args = {}    
    usernote = get_object_or_404(Usernote.objects.select_related(), id = note_id)
    if usernote.user_id != request.user.id:
        raise Http404
    
    # print 'GGGG: ', usernote.category.__dict__
    
    args['usernote'] = usernote
    return render_to_response('note_view.html',
        args,
        context_instance = RequestContext(request)
    )
