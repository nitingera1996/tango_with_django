from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from rango.models import Category,Page,UserProfile
from rango.forms import CategoryForm,PageForm,UserForm,UserProfileForm
from django.template.defaultfilters import slugify
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from registration.backends.simple.views import RegistrationView
from django.contrib.auth.models import User
from rango.bing_search import run_query

class MyRegistrationView(RegistrationView):
    def get(self):
        print self
		
def index(request):
    #request.session.set_test_cookie()
    context_dict = {}
    category_list = Category.objects.order_by('-views')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict['categories'] =category_list
    context_dict['pages']=pages_list
    visits = request.session.get('visits')
    print visits
    if not visits:
        visits = 1
    reset_last_visit_time = False
    last_visit = request.session.get('last_visit')
    print last_visit
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")		
        #print last_visit_time
        #print (datetime.now() - last_visit_time).days
        if(datetime.now() - last_visit_time).seconds > 1800:
            visits = visits + 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit']= str(datetime.now())
        request.session['visits']=visits
    context_dict['visits'] = visits	
    response = render(request,'rango/index.html',context_dict)
    return response		
	
def about(request):
    visits = request.session.get('visits')
    if not visits:
        visits = 1
    return render(request,'rango/about.html',{'visits':visits})
	
def category(request, category_name_slug):

    context_dict = {}
    context_dict['result_list']=None
    context_dict['query']=None
    if request.method=="POST":
        query=request.POST['query'].strip()
        if query:
            result_list=run_query(query)
            context_dict['result_list']=result_list
            context_dict['query']=query
    
    try:
        category = Category.objects.filter(slug=category_name_slug).order_by('name')
        category1 = Category.objects.get(slug=category_name_slug)
        context_dict['category_name']=category1.name
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages']=pages
        context_dict['category']=category1
        context_dict['category_name_slug']=category1.slug
        return render(request,'rango/category.html',context_dict)
    except Category.DoesNotExist:
        context_dict['category_name']=category_name_slug
        pass
    if not context_dict['query']:
        context_dict['query']=category.name
		
	return render(request,'rango/category.html',context_dict)

@login_required		
def add_category(request):
    if request.method == 'POST':
     	form = CategoryForm(request.POST)
        context_dict= {}
        category_name = request.POST.get('name')
        category_name_slug = slugify(category_name)
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name']=category.name
        pages = Page.objects.filter(category=category)
        context_dict['pages']=pages
        context_dict['category']=category
        context_dict['category_name_slug']=category.slug
        if form.is_valid():
            try:
                form.save(commit=True)
                return index(request)
            except:
                #return HttpResponse("Category already exist <br/> <a href = '/rango/'> Go to home </a>")
                return render(request,'rango/category.html',context_dict)
        else:
            print form.errors
    else:
        form = CategoryForm()
    return render(request,'rango/add_category.html',{'form':form})

@login_required	
def add_page(request,category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
        category_name_slug = cat.slug
    except Category.DoesNotExist:
        cat = None
		
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit = False)
                page.category = cat
                page.views = 0
                page.clean()
                page.save()
                return category(request,category_name_slug)
        else:
            print form.errors
			
    else:
        form = PageForm()
		
    context_dict = {'form': form, 'category': cat,'category_name_slug':category_name_slug}
    return render(request,'rango/add_page.html',context_dict)

def auto_add_page(request):
    if request.method == 'GET':
        cat_id = request.GET['catid']
        url = request.GET['url']
        title = request.GET['title']
    try:
        cat = Category.objects.get(id=catid)
    except Category.DoesNotExist:
        cat = None
    p = Page.objects.get_or_create(category=cat,title=title,url=url)
    pages = Page.objects.filter(category=cat).order_by('-views')
    return render(request,'rango/page_list.html',{'pages':pages})    
	
def register(request):
    #if request.session.test_cookie_worked():
     #   print ">>>> TEST COOKIE WORKED!"
      #  request.session.delete_test_cookie()

    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
		
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
            #user1 = authenticate(username = user.username,password=user.password)
            #login(request,user1)
            #return HttpResponseRedirect('/rango/')
        else :
            print user_form.errors, profile_form.errors
    else :
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,'rango/register.html',
	    {'user_form':user_form,'profile_form':profile_form,'registered':registered})
		
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        statement=None
        if not username:
            statement="Please enter the username"
        if not password and username:
            statement ="Please enter the password"
        #if username and password:
         #   us = UserProfile.objects.get(user=username)
          #  if not us:
           #     return HttpResponse("There is no user with that username")
        user = authenticate(username = username,password=password)
        if user and username and password:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username,password)
            statement="Invalid username password combination"
        if statement:
            return render(request,'rango/login.html',{'statement':statement})
    else:
        return render(request,'rango/login.html',{'statement':None})
		
@login_required
def restricted(request):
    return render(request,'rango/restricted.html')
	
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')
	
def track_url(request):
    if request.method=="GET":
        if 'pageid' in request.GET:
            pageid=request.GET['pageid']
            page=Page.objects.get(id=pageid)
            if page:
                page.views += 1
                page.save()
                return HttpResponseRedirect(page.url)
            else:
                return render(request,'rango/index.html',{})
        else:
            return render(request,'rango/index.html',{})
	    
def register_profile(request):
    registered = False
    
    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST)
        #MyRegistrationView.get()
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
            login(request,profile.user)
            return HttpResponseRedirect('/rango/')
        else :
            print user_form.errors
    else :
        profile_form = UserProfileForm()
    return render(request,'rango/profile_registration.html',
	    {'profile_form':profile_form,'registered':registered})

@login_required		
def like_category(request):
    if request.method=="GET":
        category_id=request.GET["category_id"]
        category1=Category.objects.get(id=int(category_id))
        category1.likes+=1
        category1.save()
        return HttpResponse(category1.likes)

def get_category_list(max_results=0,startswith=''):
    cat_list=[]
    #print startswith
    if startswith:
        #print "Hello"
        cat_list = Category.objects.filter(name__istartswith=startswith)
        #print cat_list1
    if max_results>0:
        if len(cat_list)>max_results:
            cat_list=cat_list[:max_results]
    return cat_list			

def suggest_category(request):
    str=request.GET["query_string"]
    #print str
    result=get_category_list(8,str)
    cat_list=[]
    for name in result:
        cat=Category.objects.get(name=name)
        cat_list.append(cat)
    #print cat_list
    return render(request,'rango/category_list.html',{'cats':cat_list})
    #return HttpResponse(cat_list)
	
@login_required
def profile(request):
    user=User.objects.get(username=request.user)
    print user
    try:
        user1=UserProfile.objects.get(user=user)
        print user1
    except:
        user1=None
    return render(request,'rango/profile.html',{'user':user,'user1':user1})
	
def search(request):
    result_list=[]
    if request.method=="POST":
        query=request.POST['query'].strip()
        if query:
            result_list=run_query(query)
			
    return render(request,'rango/search2.html',{'result_list':result_list})
