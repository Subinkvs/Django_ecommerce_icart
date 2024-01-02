from django.urls import path
from .views import *



urlpatterns = [
    path('',home.as_view(), name="index"),
    path('product/<int:product_id>',productdetail.as_view(), name = "productdetail"),
    path('category/<str:category_name>/', CategoryView.as_view(), name='category-view'),
    path('product-list', productlist.as_view()),
    path('searchproduct',searchproduct.as_view(), name='searchproduct'),
    path('add-to-cart',addtocart.as_view(), name="addtocart"),
    path('cart',cart.as_view(), name='cart' ),
    path('update-cart', updatecart.as_view(), name='updatecart'),
    path('delete-cart-item',deletecartitem.as_view(), name='deletecartitem'),
    path('wishlist', wishlist.as_view(), name='wishlist'),
    path('add-to-wishlist',addtowishlist.as_view(), name='addtowishlist'),
    path('delete-wishlist-item', deletewishlistitem.as_view(), name='deletewishlistitem'),
    path('checkoutpage', checkoutpage.as_view(), name='checkoutpage'), 
    path('place-order', placeorder.as_view(), name='placeorder'),
    path('proceed-to-pay',razorpaycheck.as_view() ),
    path('my-orders', order.as_view(), name='my-orders'),
    path('order-view/<str:t_no>',orderview.as_view(), name='order-view'),
    path('profile-view',profileview.as_view(), name='profile-view'),
    path('orders/<int:order_id>/cancel/', ordercancel.as_view(), name='ordercancel'),
    path('orderprofile', profileorder.as_view(), name='profileorder'),
    path('orderwishlist', profilewishlist.as_view(), name='profilewishlist'),
    path('store', store.as_view(), name='store'),
    path('applycoupon', applycoupon.as_view(), name='applycoupon'),
    path('contact', contactpage.as_view(), name='contactpage')
]
