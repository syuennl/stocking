from django.shortcuts import render, redirect
from django.views import View

from home import urls
from .models import Profile, Material, Product, P_Category, M_Category, Supplier, Colour, ProductMaterial
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from .forms import ProductForm, MaterialForm, UserForm, ProfileForm, RegisterForm
from django.db.models import Q
from django.contrib import messages

# Create your views here.

def loginPage(request):
    page = 'login'
    # form = UserForm()
    if request.user.is_authenticated: #restrict user frm going back to login pg by editing url
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username) # look for user obj tht matches username
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff or user.is_superuser:
                acc_type = 'adminn'
                return redirect('admin-home', acc_type)
            else:
                return redirect('home')
        else:
            messages.error(request, 'Username OR Password incorrect')

    context = {'page':page}
    return render(request, 'home/authenticate.html', context) 

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = RegisterForm() # has 3 fields: username, password, confirm password
                              # func under User model, when u submit d form, data provided = used to create new User obj

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False) # when call form.save(), converts data in the form into a model instance (here: User instance/obj)
                                             # commit = F, freeze, so we can access the user right away, so as to clean the credentials
            user.username = user.username.lower()
            user.save()

            Profile.objects.create(
                user = user,
                picture = 'user.png'
            )

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username/password during registration')

    return render(request, 'home/authenticate.html', {'form':form})

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    profile = user.profile
    products = user.product_set.all()
    materials = user.material_set.all()
    context = {'user':user, 'profile':profile, 'products':products, 'materials':materials}

    return render(request, 'home/profile.html', context)

def updateProfile(request):
    print(request.POST)
    user = request.user
    profile = Profile.objects.get(user=user)
    user_form = UserForm(instance=user)
    profile_form = ProfileForm(instance=user.profile)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            has_error = False
            new_pswrd = request.POST.get("password1").strip()
            confirm_new_pswrd = request.POST.get("password2").strip()

            if new_pswrd:
                if new_pswrd == confirm_new_pswrd:
                    user.set_password(new_pswrd)
                    update_session_auth_hash(request, user) # aft renewing pswrd, will logout user
                    user.save()
                else:
                    messages.error(request, f"Passwords do not match")
                    has_error = True

            if not has_error:
                user_form.save()
                profile_form.save()

                print("request filesssss: ", request.FILES)
                if 'picture' in request.FILES:
                    
                    profile.picture = request.FILES['picture']
                    print(request.FILES["picture"])
                    profile.save()
                    print("Saved")
                else:
                    print("no pic")
                
                # eventho ProfileForm x include picture, 
                # profile_form.save() still saves the whole Profile model 
                # may reset fields to their form values (which, for picture, would be empty)

                return redirect('profile', pk=user.id)
        
    context = {'profile':profile, 'user_form':user_form, 'profile_form':profile_form}
    return render(request, 'home/update-profile.html', context)
    
@login_required(login_url='login')
def home(request, acc_type=None): #like default value?
    print('entering home')
    print(request)

    user = request.user
    profile = Profile.objects.get(user=user)
    
    materials = Material.objects.all()
    products = Product.objects.all()

    m_categories = M_Category.objects.all()
    p_categories = P_Category.objects.all()
    all_colours = Colour.objects.all()
    all_suppliers = Supplier.objects.all()
    user = request.user

    mcat = request.GET.get('mcat', '') 
    col = request.GET.get('col', '') 
    supp = request.GET.get('supp', '') 
    # if request.GET.get('col') != None else ''
    # print("000", mcat)
    # print("000", col)
    # print("000", supp)

    # muz verify one by one cuz Q()| doesnt have hierarchy
    # if either one is "All .." will show all results
    # cuz using '|' OR not AND
    if mcat and mcat != '':
        materials = materials.filter(category__name__icontains=mcat)

    if col and col != '':
        materials = materials.filter(colour__name__icontains=col)
    
    if supp and supp != '':
        materials = materials.filter(supplier__name__icontains=supp)



    pcat = request.GET.get('pcat', '')
    if pcat and pcat != '':
        products = products.filter(category__name__icontains=pcat)
    
    #[0:5]

    # materials = Material.objects.filter(
    #     Q(category__name__icontains=mcat) |
    #     Q(colour__name__icontains=col) |
    #     Q(supplier__name__icontains=supp)
    # )  

    # products = Product.objects.filter(
    #     Q(name__icontains=q) |
    #     Q(category__name__icontains=q) |
    #     Q(materials__name__icontains=q)
    # ).distinct() #remove duplicates, 1 product w/ 3 materials wont appear 3 times #[0:5]

    # Q = an obj used to encapsulate a collection of keyword args
    # icontains, i=case insensitive
 

    context = {'materials':materials, 'products':products, 'acc_type':acc_type, 'user':user, 'profile':profile,
               'm_categories':m_categories, 'p_categories':p_categories, 'all_colours':all_colours, 'all_suppliers':all_suppliers}
    return render(request, 'home/home.html', context)

def product(request, pk, acc_type=None):
    product = Product.objects.get(id=pk)
    # product = Product.objects.prefetch_related('productmaterial_set__material').get(id=pk)
    
    details = {
            #    'picture':product.picture,
               'Name':product.name, 
               'Size':product.size, 
               'Stock':product.stock,
               'Sold':product.sold, 
               'Cost':product.cost,
               'Category':product.category,
               'Description':product.description
               }
    
    user_details = {
               'Name':product.name, 
               'Size':product.size, 
               'Cost':product.cost,
               'Category':product.category,
               'Description':product.description
               }
    
    context = {'product':product, 'details':details, 'user_details':user_details, 'acc_type':acc_type}
    return render(request, 'home/product.html', context) #can only pass one dict in render(), so include everything in context

@login_required(login_url='login')
def material(request, pk, acc_type=None):
    material = Material.objects.get(id=pk)
    obj_type = "product"

    details = {
            #    'picture':material.picture,
               'Name':material.name, 
               'Supplier':material.supplier,
               'Size':material.size, 
               'Stock':material.stock,
               'Colour':material.colour, 
               'Cost':material.cost,
               'Category':material.category,
               'Description':material.description
               }
    
    user_details = {
               'Name':material.name, 
               'Size':material.size, 
               'Stock':material.stock,
               'Colour':material.colour, 
               'Category':material.category,
               'Description':material.description
               }
    
    related_products = Product.objects.filter(materials=material)

    context = {'material':material, 'details':details, 'user_details':user_details, 
               'related_products':related_products, 'acc_type':acc_type, 'obj_type':obj_type}
    return render(request, 'home/material.html', context)

@login_required(login_url='login')
def addProduct(request):
    form = ProductForm()
    materials = Material.objects.all()
    categories = P_Category.objects.all()
    obj_type = "product"
    title = 'add new product'

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        # if form.is_valid():
        # product = form.save(commit=False) # create a Product instance, but hasn't saved 
        has_error = False

        # ---- category ----
        category_name = request.POST.get('category')
        stripped_category = category_name.strip()        
        if stripped_category != '': # not empty 
            category, created = P_Category.objects.get_or_create(name=stripped_category)
        else:
            messages.error(request, f'Please fill in the category field.')
            has_error = True

        # ---- material ----
        material_names = request.POST.getlist('productmaterial') # get list of selected materials' names frm d submitted form
        quantities_used = request.POST.getlist("quantities_used")
        valid_materials = []
        # seen_materials = set()

        # print("Received materials:", material_names)
        # print("Received quantities:", quantities_used)

        # emptyItem = (not material_names and not quantities_used) or (not material_names and len(quantities_used)==1 and quantities_used[0] == '') #list totally empty  #empty quantities_used == empty str
        # if not emptyItem:
        #     if len(material_names) != len(quantities_used): # material items incomplete
        #         messages.error(request, 'Material section incomplete')
        #         has_error = True 
        #     else: # material items complete

        for material_name, quantity in zip(material_names, quantities_used): # combine materials & quantity into tuples
            if material_name and quantity:
                try:
                    material = Material.objects.get(name=material_name) # ensure material obj exist
                    quantity = int(quantity) 
                    
                    # ensure quantity > 1
                    if quantity < 1:
                        messages.error(request, f'Quantity for {material.name} must be at least 1')
                        has_error = True
                    else:
                        valid_materials.append((material,quantity))
                
                except Material.DoesNotExist:
                    messages.error(request, f'{material_name} does not exist')
                    has_error = True
            else:
                if material_name:
                    messages.error(request, f'Please insert quantity for {material_name}')
                    has_error = True
                elif quantity:
                    messages.error(request, f'Please select a material for the provided quantity')
                    has_error = True

        if not has_error:
            # product.save()
            
            # picture
            if 'picture' in request.FILES:
                picture = request.FILES['picture']
            else:
                picture = 'product_empty.jpeg'

            product = Product.objects.create(
                # when using form.save(commit=False), x auto include values x part of form fields (e.g currently logged-in user)
                user = request.user, # muz manually link **imp
                picture = picture,
                name = request.POST.get('name'),
                size = request.POST.get('size'),
                stock = request.POST.get('stock'),
                sold = request.POST.get('sold'),
                cost = request.POST.get('cost'),
                category = category,
                description = request.POST.get('description')
            )

            if valid_materials: # if not empty item
                for material, quantity in valid_materials:
                    #create productmaterial objs
                    ProductMaterial.objects.create(
                        material = material,
                        product=product,
                        quantity_used=quantity
                    )
                    # product.materials.set(material_ids) # set() to assign materials to product, muz use set for many-to-many(?)
                    # If each material name in your database is unique, Django can implicitly use the names to match the correct Material instances. 
                    # While Django typically expects primary keys (IDs) for ManyToManyField.set(), it can also work with the field used for __str__() or unique=True fields like material names.
                    # set() method would fetch the Material objects based on the names, and link them to the product.
            
            # messages.success(request, 'Product added successfully!')
            acc_type = 'adminn'
            return redirect ('admin-home', acc_type)
    
    context = {'form':form, 'materials':materials, 'categories':categories, 'obj_type':obj_type, 'title':title}
    return render(request, 'home/form.html', context)

@login_required(login_url='login')
def addMaterial(request):
    # acc_type = 'adminn'  
    # if not request.user.is_authenticated:
    #     return redirect('home')
     
    # print('='*50)
    # print('entering add material')
    # print('req method: ', request.method)
    # print('User', request.user)
    # print('='*50)

    # if not request.user.is_staff or request.user.is_superuser:
    #     return redirect('home')
    
    form = MaterialForm()
    categories = M_Category.objects.all()
    suppliers = Supplier.objects.all()
    colours = Colour.objects.all()
    obj_type = "material"
    title = 'add new material'

    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        # if form.is_valid():
        # material = form.save(commit=False)
        # user = request.user
        has_error = False

        # ---- category ----
        category_name = request.POST.get('category')
        stripped_category = category_name.strip()
        if stripped_category != '': # not empty 
            category, created = M_Category.objects.get_or_create(name=stripped_category)
        else:
            messages.error(request, f'Please fill in the category field.')
            has_error = True

        # ---- supplier ----
        supplier_name = request.POST.get('supplier')
        stripped_supplier = supplier_name.strip()
        if stripped_supplier != '':
            supplier, created = Supplier.objects.get_or_create(name=stripped_supplier)
        else:
            messages.error(request, f'Please fill in the supplier field.')
            has_error = True

        # ---- colour ----
        colour_name = request.POST.get('colour')
        stripped_colour = colour_name.strip()
        if stripped_colour != '':
            colour, created = Colour.objects.get_or_create(name=stripped_colour)
        else:
            messages.error(request, f'Please fill in the colour field.')
            has_error = True

        # material.save()

        if not has_error:
            if 'picture' in request.FILES:
                picture = request.FILES['picture']
            else:
                picture = 'material_empty.jpeg'

            Material.objects.create(
                user = request.user,
                picture = picture,
                name = request.POST.get('name'),
                supplier = supplier,
                size = request.POST.get('size'),
                stock = request.POST.get('stock'),
                colour = colour,
                cost = request.POST.get('cost'),
                description = request.POST.get('description'),
                category = category
            )

            acc_type = 'adminn'
            return redirect ('admin-home', acc_type)
    
    context = {'form':form, 'categories':categories, 'suppliers':suppliers, 'colours':colours, 'obj_type':obj_type, 'title':title}
    return render(request, 'home/form.html', context)

@login_required(login_url='login')
def updateProduct(request, pk):
    obj = Product.objects.get(id=pk)
    obj_type = "product"
    form = ProductForm(instance=obj)
    title = 'update ' + obj.name
    
    categories = P_Category.objects.all()
    materials = Material.objects.all()
    productMaterial = ProductMaterial.objects.filter(product=obj) # "get" oni returns 1 obj, "filter" returns >=1

    if request.method == 'POST':
        # form = ProductForm(request.POST, request.FILES, instance=obj) 
        # if form.is_valid():
        #     form.save()

        has_error = False

        # ---- category ----
        category_name = request.POST.get('category')
        stripped_category = category_name.strip()
        if stripped_category != '': # not empty 
            category, created = P_Category.objects.get_or_create(name=stripped_category)
        else:
            messages.error(request, f'Please fill in the category field.')
            has_error = True

        # ---- materials ----
        material_names = request.POST.getlist('productmaterial')
        quantities_used = request.POST.getlist('quantities_used')
        # print("materials : ", material_names)
        # print("quantities used: ", quantities_used)

        valid_materials = []
        
        for material_name, quantity in zip(material_names, quantities_used):
            if material_name and quantity: # ensure not null values
                try:
                    material = Material.objects.get(name=material_name) #ensure material obj exist
                    quantity = int(quantity) 
                    
                    #ensure quantity > 1
                    if quantity < 1:
                        messages.error(request, f'Quantity for {material.name} must be at least 1')
                        has_error = True
                    else:
                        valid_materials.append((material,quantity))
                    
                except Material.DoesNotExist:
                    messages.error(request, f'{material_name} does not exist')
                    has_error = True
            else:
                if material_name:
                    messages.error(request, f'Please insert quantity for {material_name}')
                    has_error = True
                elif quantity:
                    messages.error(request, f'Please select a material for the provided quantity')
                    has_error = True
         
        if not has_error:
            # delete existing materials, replace wif new ones
            ProductMaterial.objects.filter(product=obj).delete()
            for material, quantity in valid_materials:
                ProductMaterial.objects.create(
                            material=material,
                            product=obj,
                            quantity_used=quantity
                        )

            if 'picture' in request.FILES:
                # print(request.FILES['picture'])
                obj.picture = request.FILES['picture']

            obj.name = request.POST.get('name')
            obj.size = request.POST.get('size')
            obj.stock = request.POST.get('stock')
            obj.sold = request.POST.get('sold')
            obj.cost = request.POST.get('cost')
            obj.category = category
            obj.description = request.POST.get('description')

            obj.save()
            acc_type = 'adminn'
            return redirect ('admin-product', pk, acc_type)    
    
    context = {'form':form, 'obj':obj, 'obj_type':obj_type, 'categories':categories, 'materials':materials, 'productMaterial':productMaterial, 'title': title}
    return render(request, 'home/form.html', context)

@login_required(login_url='login')
def updateMaterial(request, pk):
    obj = Material.objects.get(id=pk)
    obj_type = "material"
    form = MaterialForm(instance=obj)
    title = 'update ' + obj.name

    categories = M_Category.objects.all() # all options will b rendered in the form
    suppliers = Supplier.objects.all()
    colours = Colour.objects.all()

    if request.method == 'POST':
        has_error = False
        # form = MaterialForm(request.POST, request.FILES, instance=obj) 
        # if form.is_valid():
        #     material = form.save(commit=False) #freeze

        if 'picture' in request.FILES:
            # print(request.FILES['picture'])
            picture = request.FILES['picture']
    
        # obj.picture = request.FILES.get('picture')
        # obj.name = request.POST.get('name')

        # ---- colour ----
        colour_name = request.POST.get('colour')
        stripped_colour = colour_name.strip()
        if stripped_colour != '': # not empty 
            colour, created = Colour.objects.get_or_create(name=stripped_colour)
        else:
            messages.error(request, f'Please fill in the colour field.')
            has_error = True

        # ---- supplier ----
        supplier_name = request.POST.get('supplier')
        stripped_supplier = supplier_name.strip()
        if stripped_supplier != '': 
            supplier, created = Supplier.objects.get_or_create(name=stripped_supplier)
        else:
            messages.error(request, f'Please fill in the supplier field.')
            has_error = True

        # ---- category ----
        category_name = request.POST.get('category')
        stripped_category = category_name.strip()
        if stripped_category != '':
            category, created = M_Category.objects.get_or_create(name=stripped_category)
        else:
            messages.error(request, f'Please fill in the category field.')
            has_error = True

        # obj.save() # imp  
        if not has_error: 
            obj.picture = request.FILES['picture']
            obj.name = request.POST.get('name') # names are auto added to attributes in form.html during render of form
            obj.size = request.POST.get('size')
            obj.stock = request.POST.get('stock')
            obj.colour = colour
            obj.cost = request.POST.get('cost')
            obj.supplier = supplier
            obj.category = category
            obj.description = request.POST.get('description')  

            obj.save()
            acc_type = 'adminn'
            return redirect ('admin-material', pk, acc_type)
       
    context = {'form':form, 'obj':obj, 'obj_type':obj_type, 'categories':categories, 'suppliers':suppliers, 'colours':colours, 'title': title}
    return render(request, 'home/form.html', context)

@login_required(login_url='login')
def delete(request, obj_type, pk):
    if obj_type == 'Product':
        obj = Product.objects.get(id=pk)
    elif obj_type == "Material":
        obj = Material.objects.get(id=pk)
    else:
        obj = None

    if request.method == 'POST' and obj:
        obj.delete()
        return redirect('admin-home', 'adminn')
        
    return render(request, 'home/delete.html', {'obj':obj})

def increase(request, obj_type, pk):
    if obj_type == 'material':
        obj = Material.objects.get(id=pk)
    elif obj_type == 'product':
        obj = Product.objects.get(id=pk)
    else:
        obj = None

    if obj:
        obj.stock += 1
        obj.save()
    return redirect(obj_type, pk)

def decrease(request, obj_type, pk):
    if obj_type == 'material':
        obj = Material.objects.get(id=pk)
    elif obj_type == 'product':
        obj = Product.objects.get(id=pk)   
    else:
        obj = None

    if obj:  
        obj.stock -= 1 
        obj.save()
    return redirect(obj_type, pk) 

