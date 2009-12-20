# Create your views here.
from django.http import Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
from couchdb.client import ResourceNotFound
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required

DB=settings.DB

def home(request, pageno=0):
    next=prev=None
    pageno=int(pageno)
    endkey = DB['counter']['value']-1 - (10*pageno)
    posts = [e.value for e in DB.view('_design/views/_view/posts',
                    startkey=endkey, limit=11, descending=True).rows]
    if len(posts) > 10:
        prev = u'%d' % (pageno+1,)
    if pageno > 0:
        next = u'%d' % (pageno-1,)

    posts=posts[:10]
    return render_to_response('postList.html', {'posts':posts, 'hasNext':next,
                                                'hasPrev':prev})

@login_required
def add_post(request):
    title = request.POST.get('title')
    author = request.user.username
    markdown = request.POST.get('markdown')
    html = request.POST.get('html')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    summary = markdown[:200]
    id = DB['counter']['value']+1
    DB.delete(DB['counter'])
    DB['counter'] = {'value':id+1}
    slug = '/'+author+'/'+slugify(title)+'/'+str(id)
    DB[str(id)]={'title':title, 'author':author, 'markdown':markdown,
                 'html':html, 'timestamp':timestamp, 'slug':slug,
                 'summary':summary}
    return HttpResponseRedirect('/post/'+slug)

@login_required
def edit_post(request):
    title = request.POST.get('title')
    author = request.user.username
    markdown = request.POST.get('markdown')
    html = request.POST.get('html')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    summary = markdown[:200]
    post = DB.view('_design/views/_view/post_by_slug', key=request.path).rows[0].value
    id = post['_id']
    DB.delete(DB[id])
    slug = '/'+author+'/'+slugify(title)+'/'+id
    DB[id]={'title':title, 'author':author, 'markdown':markdown,
            'html':html, 'timestamp':timestamp, 'slug':slug, 'summary':summary}
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

def get_post(request, username, title, id):
    slug = '/'.join([username, title, id])
    doc = DB.view('_design/views/_view/post_by_slug', key=slug).rows[0].value
    return render_to_response('post.html', doc)




