from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm,card_lookup,AddRecordForm,price_edit,image_upload,SearchForm
from .models import Record,card_user_table,grader_names,team_names
from .funcs import lookup_card,create_search_query,add_record_to_db,get_s3_url
from django.contrib.auth.models import User 
from decimal import Decimal
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.core.files.uploadedfile import TemporaryUploadedFile

# Create your views here.
MESSAGE_TAGS = {
    messages.INFO: ""
}

def image_uploader(request):
    if request.method == 'POST':
        form = image_upload(request.POST, request.FILES)
        print(form.files)
        if form.is_valid():
            uploaded_image = str(form.cleaned_data['image']).replace(' ','_')
            print(form.cleaned_data['image'])
            url = get_s3_url(f'images/{uploaded_image}')
            print(url)

           
            form.save()
            return render(request, 'image_upload.html', {'form': form,'img_url':url})
        else:
            messages.success(request=request, message="Failed to update image")
            return render(request, 'image_upload.html', {'form': form})
    else:
        form = image_upload()
    return render(request, 'image_upload.html', {'form': form})



def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request,username=username,password=password)

        if user is not None:
            login(request=request,user=user)
            messages.success(request=request, message="You have been successfully logged in")
            return redirect('home')
        else:
            messages.success(request=request, message="Failed to logged in")
            return redirect('home')
    else:
        queryset = card_user_table.objects.filter(user_id=request.user.id).order_by('-average_price')
        if len(queryset)>0:
            items_per_page = 5
            paginator = Paginator(queryset, items_per_page)
            page = request.GET.get('page')
            try:
                items = paginator.page(page)
            except EmptyPage:
                items = paginator.page(paginator.num_pages)
            except PageNotAnInteger:
                items = paginator.page(1)
            return render(request, 'home.html',{'records':queryset,'page':page, 'items':items})
        else:
            return render(request, 'home.html')

def logout_user(request):
    logout(request=request)
    messages.success(request=request, message="You have been logged out")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request=request,user=user)
            messages.success(request=request, message="You have successfully registered")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request=request,template_name='register.html',context={'form':form})
    return render(request=request,template_name='register.html',context={'form':form})


def card_lookup_page(request):
    user_id = request.user.id
    if request.method == 'POST':
        img_form = image_upload(request.POST, request.FILES)
        if 'search' in request.POST: 
            form = card_lookup(request.POST)
            
            if form.is_valid():
                search_query = create_search_query(form=form,user_id=user_id)  
                request.session['lookup_data'] = search_query[1]
                print(search_query)
                results = lookup_card(search_query[0])
                print(results)
                if results is not None:
                    bad_search = False
                    price = results['average_price']
                    print(price)
                    initial ={
                        'price_field':price
                    }
                    price_form = price_edit(initial=initial)
                    results['search_crit'] = results['search_crit'].replace('+',' ')
                else:
                    results = None
                    bad_search = True
                    price_form = price_edit()
                # print(search_query[1])
                
                

                
                request.session['result_data'] = results
    
                return render(request=request, template_name='card_lookup.html',context={'form':form, 'results':results, 'search_query':search_query[0],'bad_search':bad_search,'price_form':price_form,'img_form':img_form})
               
        if 'add' in request.POST:
            print('adding..')
            
            price = Decimal(price_edit(request.POST).data.get('price_field'))
            search_data = request.session['lookup_data']
            result_data = request.session['result_data']
            print(len(img_form.files))
            if img_form.is_valid() and len(img_form.files)>0:
                if len(img_form.files['image']) > 0:
                    uploaded_image = str(img_form.files['image']).replace(' ','_')
                    img_url = get_s3_url(f'images/{uploaded_image}')   
                    request.session['result_data']['img']=img_url
                    img_form.save()
                result_data['average_price'] = price
            form = card_lookup()
            
            add_record_to_db(search_data=request.session['lookup_data'],result_data=request.session['result_data'])
            messages.success(request=request, message="Card Added")
            return render(request=request, template_name='card_lookup.html',context={'form':form})

    else:
        form = card_lookup()
    return render(request=request, template_name='card_lookup.html',context={'form':form})

        
    
    


def customer_record(request,pk):
    if request.user.is_authenticated:
        previous_url = request.META.get('HTTP_REFERER')
        customer_record = card_user_table.objects.get(card_id=pk)
        
        return render(request=request, template_name='record.html',context={'customer_record':customer_record, 'previous_url':previous_url})
    else:
        messages.success(request=request, message="You must be logged in")
        return redirect('home')
    
def delete_card(request,pk):
    if request.user.is_authenticated:
        delete_it = card_user_table.objects.get(card_id=pk)
        delete_it.delete()
        messages.success(request=request, message="Record Deleted")
        return redirect('home')
    else:
        messages.success(request=request, message="You must be logged in")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            print(request.session['my_data'])
            if form.is_valid():
                add_record = form.save()
                messages.success(request=request, message="Record Added")
                return redirect('home')

        return render(request=request, template_name='add_record.html',context={'form':form})
    else:
        messages.success(request=request, message="You must be logged in")
        return redirect('home')

def update_record(request,pk):
     if request.user.is_authenticated:
         current_record = Record.objects.get(id=pk)
         form = AddRecordForm(request.POST or None, instance=current_record)
         if form.is_valid():
             form.save()
             messages.success(request=request, message="Record Updated")
         return render(request=request, template_name='update_record.html',context={'form':form})
     else:
        messages.success(request=request, message="You must be logged in")
        return redirect('home')
     

def search_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            # Perform the search based on the search_query
            # You can use the search_query to filter your data
            # and render the results in the template
            return render(request, 'results.html', {'search_query': search_query})
    else:
        form = SearchForm()
    
    return render(request, 'search.html', {'form': form})