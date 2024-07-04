# have an error when type int have an error 
from store.models import Product,Profile

class Cart():
    def __init__(self,request):
        self.session = request.session
        #GET request
        self.request = request
        #Get the current session key if it exists
        cart = self.session.get('session_key')

        #if the user is new, no session key! create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        
        #Make sure cart is avaliable on all pages of site
        self.cart = cart
    def db_add(self,product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        #logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price' : str(product.price)}
            self.cart[product_id] = str(product_qty)
        self.session.modified = True 

        #Deal with logged in user
        if self.request.user.is_authenticated:
            #GET THE CURRENT USER PROFILE
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            #save carty to the profile model
            current_user.update(old_cart=str(carty))
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        #logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price' : str(product.price)}
            self.cart[product_id] = str(product_qty)
        self.session.modified = True 

        #Deal with logged in user
        if self.request.user.is_authenticated:
            #GET THE CURRENT USER PROFILE
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            #save carty to the profile model
            current_user.update(old_cart=str(carty))

    def __len__(self):
        return len(self.cart)
    def get_prods(self):
        #GET ids from cart
        product_ids = self.cart.keys()
        #Use ids to lookup products in database model
        products = Product.objects.filter(id__in = product_ids)
        #RETURN those looked up
        return products
    def get_quants(self):
        quantities = self.cart
        return quantities
    def update(self,product,quantity):
        product_id = str(product)
        product_qty = int(product.quantity)

        #Get cart 
        ourcart = self.cart
        #Update Dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True
        thing = self.cart
        return thing
    def delete(self, product):
        product_id = str(product)
        # Delete from dicitionary/cart
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
        if self.request.user.is_authenticated:
            #GET THE CURRENT USER PROFILE
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            #save carty to the profile model
            current_user.update(old_cart=str(carty))
