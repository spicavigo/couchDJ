# Create your views here.
from django.http import Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
from couchdb.client import ResourceNotFound
from django.conf import settings
from django.template.defaultfilters import slugify

DB=settings.DB

def home(request, page_no):
    next=prev=None
    endkey = DB['counter']-1 - (10*int(pge_no))
    posts = [e.value for e in DB.view('_design/views/_view/posts',
                    endkey=endkey, limit=11, descending=True).rows]
    if len(posts) > 10:
        next = request.path + '?pageno=%d' % pageno+1
    if page_no > 0:
        prev = request.path + '?pageno=%d' % pageno-1

    posts=posts[:10]
    return render_to_response('home', {'posts':posts, 'next':next, 'prev'=prev})


@login_required
def add_post(request):
    title = request.POST.get('title')
    author = request.user.username
    markdown = request.POST.get('markdown')
    html = request.POST.get('html')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    id = DB['counter']['value']+1
    DB.delete(DB['counter'])
    DB['counter'] = {'value':id+1}
    slug = '/'+author+'/'+slugify(title)+'/'+str(id)
    DB[str(id)]={'title':title, 'author':author, 'markdown':markdown,
                 'html':html, 'timestamp':timestamp, 'slug':slug}
    return HttpResponseRedirect('/post/'+slug)

@login_required
def edit_post(request):
    title = request.POST.get('title')
    author = request.user.username
    markdown = request.POST.get('markdown')
    html = request.POST.get('html')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    post = DB.view('_design/views/_view/post_by_slug', key=request.path).rows[0].value
    id = post['_id']
    DB.delete(DB[id])
    slug = '/'+author+'/'+slugify(title)+'/'+id
    DB[id]={'title':title, 'author':author, 'markdown':markdown,
                    'html':html, 'timestamp':timestamp, 'slug':slug}
    return HttpResponse('/post/'+slug)

def add_comment(request):
    title = request.POST.get('title')
    author = request.POST.get('name')
    markdown = request.POST.get('markdown')
    html = request.POST.get('html')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    post = DB.view('_design/views/_view/post_by_slug',
                   key=request.POST.get('post_path')).rows[0].value['_id']
    id=DB['commentcounter']['value']+1
    DB.delete(DB['commentcounter'])
    DB['commentcounter'] = {'value':id+1}
    DB['comment-'+str(id)] = {'title':title, 'author':author,
                              'markdown':markdown, 'html':html,
                              'timestamp':timestamp, 'post': post}
    return HttpResponse('ok')

def get_post(request, slug):
    doc = DB.view('_design/views/_view/post_by_slug', key=slug).rows[0].value
    return render_to_response('post.html', doc)




