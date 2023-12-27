from django.shortcuts import render, redirect,HttpResponse,reverse
from .models import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from accounts.models import User
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views import View
from django.utils import timezone
import random
#  Create your views here. 

# To render the landing page of the project
class home(View):
    template_name = 'index.html'
    
    def get_context_data(self,request):
        prods = MenClothing.objects.filter(is_featured=True)
        bannerimage = BannerImage.objects.all()
        cartitem = Cart.objects.filter(user=self.request.user.id)
        total_quantity = sum(item.product_qty for item in cartitem)
        wishlist = Wishlist.objects.filter(user=request.user.id)
        total_item =len(wishlist)
        
        context = {
            'prods': prods,
            'bannerimage': bannerimage,
            'cartitem': cartitem,
            'total_quantity': total_quantity,
            'total_item':total_item
            
        }

        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context) 

# To get product details of each product
class productdetail(View):
    template_name = 'product-detail.html'
    
    def get_context_data(self,request, product_id):
        product = get_object_or_404(MenClothing, pk=product_id)
        cartitem = Cart.objects.filter(user=self.request.user.id)
        total_quantity = sum(item.product_qty for item in cartitem)
        wishlist = Wishlist.objects.filter(user=request.user.id)
        total_item =len(wishlist)
        context = {
            'product': product,
            'cartitem': cartitem,
            'total_quantity': total_quantity,
             'total_item': total_item
        }

        return context

    def get(self, request, product_id):
        context = self.get_context_data(request,product_id)
        return render(request, self.template_name, context)


# To get the category page separatly
class CategoryView(View):
    template_name = 'category.html'
    def get_context_data(self,request, category_name):
        predefined_categories = ['T-shirt','Shirt','Jacket','Jeans']
        if category_name:
            category_items = MenClothing.objects.filter(category__name__iexact=category_name, is_featured=True)
        else:
            category_items = MenClothing.objects.filter(category__name__iexact__in=predefined_categories, is_featured=True)

        cart_items = Cart.objects.filter(user=self.request.user.id)
        total_quantity = sum(item.product_qty for item in cart_items)
        wishlist = Wishlist.objects.filter(user=request.user.id)
        total_item =len(wishlist)

        context = {
            'categories': predefined_categories,
            'category_name': category_name,
            'products': category_items,
            'total_quantity': total_quantity,
            'total_item': total_item
        }

        return context
    '''To get the category page separatly'''
    
    def get(self, request, category_name=None):
        context = self.get_context_data(request,category_name)
        return render(request, self.template_name, context)
 
# To add product to the cart
class addtocart(View):
    '''Add product to the cart'''
    def post(self, request):
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = MenClothing.objects.get(id=prod_id)

            if product_check:
                if Cart.objects.filter(user=request.user.id, product_id=prod_id).exists():
                    return JsonResponse({'status': 'Product Already in Cart'})
                else:
                    prod_qty = int(request.POST.get('product_qty'))

                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                        return JsonResponse({'status': 'Product added successfully'})
                    else:
                        return JsonResponse({'status': f'Only {product_check.quantity} quantity available'})
            else:
                return JsonResponse({'status': 'No such product found'})
        else:
            return JsonResponse({'status': 'Please Login to Continue'})

    def get(self, request):
        return redirect('index')

#To view cart page
class cart(View):
    '''To view cart page'''
    def get(self, request):
        if request.user.is_authenticated:
            cartitem = Cart.objects.filter(user=request.user.id).order_by('-created_at')
            total_quantity = sum(item.product_qty for item in cartitem)
            sub_total = sum(item.product.price * item.product_qty for item in cartitem)
            delivary_charge = 0
        
            
            # Retrieve applied coupon information from the session
            coupon_code =request.session.get('coupon_code')
            discount = request.session.get('discount', 0)
            
            # if sub_total >= 5000:
            #     messages.success(request, "Your Shipping charge is free now..!")
            
            # Delivary charge is only applied when cart is not empty
            if total_quantity > 0:
                delivary_charge = 50
            
            if sub_total <= 5000 and total_quantity > 0 :
                total_price = sub_total + delivary_charge
                
                   
            # Check if the discount is applied (coupon_code is present)
            # Calculate total price after applying the coupon discount with delivary charge
            if coupon_code and sub_total <= 5000:      
                total_price = (sub_total - discount) + delivary_charge
             
            # If coupon is applied, sub_total is greater than 5000 Rs.
            # Calculate total price after applying the coupon discount
            elif coupon_code and sub_total >= 5000:
                total_price = sub_total - discount
                
            # If no coupon is applied, check sub_total is less than or equal to 5000 Rs.
            # Calculate total price with devilary charge and discount is zero.    
            elif sub_total <= 5000:
                total_price = sub_total + delivary_charge
                discount = 0  
            else:
                total_price = sub_total
                discount = 0
                
            
            wishlist = Wishlist.objects.filter(user=request.user.id)
            total_item =len(wishlist)

            context = {'cartitem': cartitem, 
                       'total_quantity': total_quantity, 
                       'sub_total': sub_total,
                       'total_item':total_item, 
                       'discount':discount, 
                       'total_price':total_price,
                       'coupon_code':coupon_code,
                       'delivary_charge':delivary_charge
                       }
            return render(request, 'cart.html', context)
        else:
             return redirect('loginpage')
         
    
         
# To update the product quantity in the cart
class updatecart(View):
    '''To update the product quantity in the cart'''
    def post(self, request):
        prod_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user=request.user.id, product_id=prod_id).exists():
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id, user=request.user.id)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status': 'Updated Successfully'})
        return redirect('index')


# To delete the product added in the cart
class deletecartitem(View):
    '''To delete the product added in the cart'''
    def post(self, request):
        prod_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user=request.user, product_id=prod_id).exists():
            cartitem = Cart.objects.get(product_id=prod_id, user=request.user)
            cartitem.delete()
        
        # Clear coupon-related session variables after placing the order
        if 'coupon_code' in request.session:
            del request.session['coupon_code']
        if 'discount' in request.session:
            del request.session['discount']  
             
            return JsonResponse({'status': 'Deleted Successfully'})
        return redirect('index')


# To view the Wishlist page
class wishlist(View):
    ''' To view the Wishlist page'''
    def get(self, request):
        if request.user.is_authenticated:
            cartitem = Cart.objects.filter(user=self.request.user.id)
            total_quantity = sum(item.product_qty for item in cartitem)
            wishlist = Wishlist.objects.filter(user=request.user.id)
            total_item =len(wishlist)
            context = {'wishlist': wishlist, 'total_quantity': total_quantity,'total_item':total_item}
            return render(request, 'wishlist.html', context)
        else:
            return redirect('loginpage')


# To add the product to the wishlist
class addtowishlist(View):
    '''To add the product to the wishlist'''
    def post(self, request):
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = MenClothing.objects.get(id=prod_id)
            if product_check:
                if Wishlist.objects.filter(user=request.user, product_id=prod_id):
                    return JsonResponse({'status': 'Product already in wishlist'})
                else:
                    Wishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status': 'Product added to wishlist'})
            else:
                return JsonResponse({'status': 'No such product found'})
        else:
            return JsonResponse({'status': 'Please Login to continue'})
               

# To delete product from the deletewishlistitem
class deletewishlistitem(View):
    '''To add the product to cart'''
    def post(self, request):
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            if Wishlist.objects.filter(user=request.user, product_id=prod_id).exists():
                wishlistitem = Wishlist.objects.get(user=request.user, product_id=prod_id)
                wishlistitem.delete()
                return JsonResponse({'status': 'Product removed from wishlist'})
            else:
                return JsonResponse({'status': 'Product not found in wishlist'})
        else:
            return JsonResponse({'status': 'Please Login to continue'})
        
    def get(self, request):
        return redirect('index')

# To view checkout page
class checkoutpage(View):
    ''' To view checkout page'''
    def get(self, request):
        rawcart = Cart.objects.filter(user=request.user)
        total_quantity = sum(item.product_qty for item in rawcart)
        
        
        for item in rawcart:
            if item.product_qty > item.product.quantity:
                item.delete()

        cartitems = Cart.objects.filter(user=request.user)
        sub_total = sum(item.product.price * item.product_qty for item in cartitems)
        delivary_charge = 50
        # Retrieve applied coupon information from the session
        discount = request.session.get('discount', 0)
        
        # Calculate total price after applying the coupon discount with delivary charge and sub_total
        if sub_total >= 5000:
            total_price = sub_total - discount
        else:
            total_price = (sub_total - discount) + delivary_charge
         
        
        userprofile = Profile.objects.filter(user=request.user).first()
        wishlist = Wishlist.objects.filter(user=request.user.id)
        total_item =len(wishlist)

        context = {'cartitems': cartitems, 'total_price': total_price, 'total_quantity': total_quantity, 'userprofile': userprofile, 'total_item':total_item}
        return render(request, 'place-order.html', context)


# To placeorder a product
class placeorder(View):
    '''To placeorder a product'''
    def post(self, request):
        currentuser = User.objects.filter(id=request.user.id).first()
        
        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('firstname')
            currentuser.last_name = request.POST.get('lastname')
            currentuser.save()
            
        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()
            
        neworder = Order()
        neworder.user = request.user
        neworder.firstname = request.POST.get('firstname')
        neworder.lastname = request.POST.get('lastname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')
        
        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')
        cart = Cart.objects.filter(user=request.user)
        discount = request.session.get('discount', 0)
        cart_total_price = sum(item.product.price * item.product_qty for item in cart) - discount
        sub_total = sum(item.product.price * item.product_qty for item in cart)
        delivary_charge = 50
        
        # Add Shipping charge if the sub total is less than 5000 Rs
        if sub_total <= 5000:
            cart_total_price = cart_total_price + delivary_charge
         
        # Clear coupon-related session variables after placing the order
        if 'coupon_code' in request.session:
            del request.session['coupon_code']
        if 'discount' in request.session:
            del request.session['discount']
        
        neworder.total_price = cart_total_price
        trackno = 'Hello' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = 'Hello' + str(random.randint(1111111, 9999999))
            
        neworder.tracking_no = trackno
        neworder.save()
        
        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.price,
                quantity=item.product_qty
            )
            
            orderproduct = MenClothing.objects.filter(id=item.product_id).first()
            orderproduct.quantity = orderproduct.quantity - item.product_qty
            orderproduct.save()
        
        Cart.objects.filter(user=request.user).delete()
        messages.success(request, "Your Order has be placed successfully")
        
        payMode = request.POST.get('payment_mode')
        if(payMode == "Paid by Razorpay"):
            return JsonResponse({'status': "Your Order has be placed successfully"})
        return redirect('index')
  
    
# To see all products using pagination
class store(View):
    '''To see all products using pagination'''
    def get(self, request):
        prods = MenClothing.objects.all().order_by('image')
        cartitem = Cart.objects.filter(user=request.user.id)
        total_quantity = sum(item.product_qty for item in cartitem)
        wishlist = Wishlist.objects.filter(user=request.user.id)
        total_item =len(wishlist)
        category = Category.objects.all()
        paginator = Paginator(prods, 3)
        page = request.GET.get('page')
        
        try:
            prods = paginator.page(page)
        except PageNotAnInteger:
            prods = paginator.page(1)
        except EmptyPage:
            prods = paginator.page(paginator.num_pages)
        
        context = {'prods': prods, 'page': page, 'category': category, 'total_quantity': total_quantity,'total_item': total_item}
        return render(request, 'store.html', context)
 
  
#  To list product in the searchbar  
class productlist(View):
    ''' To list product in the searchbar '''
    def get(self, request, *args, **kwargs):
        products = MenClothing.objects.all().values_list('name', flat=True)
        productList = list(products)
        return JsonResponse(productList, safe=False)

    
# To search product from the search bar   
class searchproduct(View):
    '''To search product from the search bar '''
    def post(self, request):
        searchedterm = request.POST.get('productsearch')
        
        if searchedterm == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = MenClothing.objects.filter(name__contains=searchedterm).first()
            if product:
                return redirect('product/' + str(product.id))
            else:
                messages.info(request, "No product matched your search")
                return redirect(request.META.get('HTTP_REFERER'))

    def get(self, request):
        # Handle GET requests if needed
        return redirect(request.META.get('HTTP_REFERER'))
    
# To add Razorpaycheck payment    
class razorpaycheck(View):
    '''To add Razorpaycheck payment '''
    def get(self,request,*args, **kwargs):
        cart = Cart.objects.filter(user=request.user)
         
        # Retrieve applied coupon information from the session
        discount = request.session.get('discount', 0)
       
        total_price = sum(item.product.price * item.product_qty for item in cart) - discount
        sub_total = sum(item.product.price * item.product_qty for item in cart)
        delivary_charge = 50
        
        # Calculate the total_price if the sub_total is less than 5000 Rs.
        if sub_total <= 5000:
            total_price = total_price + delivary_charge
        
        
        return JsonResponse({
            'total_price':total_price
        })

# To view order history      
class order(View):
    '''To view order with relevant status'''
    def get(self,request,*args, **kwargs):
        orders = Order.objects.filter(user=request.user.id) 
        total_items = len(orders)
        cartitem = Cart.objects.filter(user=request.user.id)
        total_quantity = sum(item.product_qty for item in cartitem)
        wishlist = Wishlist.objects.filter(user=request.user.id)
        total_item =len(wishlist)
        discount = request.session.get('discount', 0)            
        context = {
            'orders':orders,
            'total_item':total_item,
            'total_quantity':total_quantity,
            'total_items':total_items,
            'discount':discount
        }
        return render(request,'order.html', context)
    
# To view the order details
class orderview(View):
    '''To view order details '''
    def get(self,request,t_no,*args, **kwargs):
        order = Order.objects.filter(tracking_no=t_no).filter(user=request.user.id).first()
        orderitems = OrderItem.objects.filter(order=order)
        cartitem = Cart.objects.filter(user=request.user.id)
        total_quantity = sum(item.product_qty for item in cartitem)
        wishlist = Wishlist.objects.filter(user=request.user.id)
        total_item =len(wishlist)
        context = {
            'order':order,
            'orderitems':orderitems,
            'total_item':total_item,
            'total_quantity':total_quantity
        }
        return render(request, 'orderview.html', context )
 
# To view profile for the user   
class profileview(View):
    '''To view the profile of the user'''
    def get(self,request,*args, **kwargs):
        profile = Profile.objects.filter(user=request.user).first()
        orders = Order.objects.filter(user=request.user.id)
        total_items = len(orders)
        cartitem = Cart.objects.filter(user=self.request.user.id)
        total_quantity = sum(item.product_qty for item in cartitem)
        total_price = sum(item.product.price * item.product_qty for item in cartitem)
        wishlist = Wishlist.objects.filter(user=request.user.id)
        total_item =len(wishlist)
        context = {
            'profile': profile,
            'orders':orders,
            'total_items':total_items,
            'total_quantity':total_quantity,
            'total_item':total_item,
            'cartitem':cartitem,
            'total_price':total_price,
            'wishlist':wishlist
        }
        return render(request, 'dashboard.html', context)
    
# To cancel your order from my orders
class ordercancel(View):
    '''To cancel the order in pending stage'''
    def post(self,request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        if order.status:
            order.delete()
            return JsonResponse({'status': 'Your Order Cancelled Successfully'})
        return JsonResponse({'status': 'Cancellation not allowed'})
      
# To view order history from profile page
class profileorder(View):
    '''To view order history from profile page'''
    def get(self,request,*args, **kwargs):
        orders = Order.objects.filter(user=request.user.id) 
        total_items = len(orders)
        cartitem = Cart.objects.filter(user=request.user.id)
        total_quantity = sum(item.product_qty for item in cartitem)
        wishlist = Wishlist.objects.filter(user=request.user.id)
        total_item =len(wishlist)              
        context = {
            'orders':orders,
            'total_item':total_item,
            'total_quantity':total_quantity,
            'total_items':total_items
        }
        
        return render(request, 'profileorder.html', context)
 
# To view wishlist from profile page
class profilewishlist(View):
    '''To view wishlist from profile page'''
    def get(self, request):
        if request.user.is_authenticated:
            cartitem = Cart.objects.filter(user=self.request.user.id)
            total_quantity = sum(item.product_qty for item in cartitem)
            wishlist = Wishlist.objects.filter(user=request.user.id)
            total_item =len(wishlist)
            context = {'wishlist': wishlist, 'total_quantity': total_quantity,'total_item':total_item}
        return render(request, 'profilewishlist.html', context)
 
    
# To apply coupon code and discount price in shopping cart page
class applycoupon(View):
    '''To apply coupon code and discount price in shopping cart page'''
    template_name = 'cart.html'

    def post(self, request, *args, **kwargs):
        coupon_code = request.POST.get('coupon_code')

        try:
            coupon = Coupon.objects.get(code__iexact=coupon_code)
        except Coupon.DoesNotExist:
            messages.error(request, 'Please check the coupon code..it does not exist.')
            return redirect(reverse('cart'))

        if coupon.valid_from <= timezone.now() <= coupon.valid_to:
            if 'coupon_code' in request.session:
                messages.warning(request, "Your coupon is already applied.")
            else:
                request.session['coupon_code'] = coupon_code
                request.session['discount'] = coupon.discount
                messages.success(request, 'Your coupon applied successfully.')
        else:
            messages.error(request, 'The coupon code is not valid or expired.')

        return redirect(reverse('cart'))

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
        