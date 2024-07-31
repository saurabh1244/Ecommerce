import decimal
from store.models import Product , Profile

class Cart():
    def __init__(self, request):
        self.session = request.session

        self.request = request

        cart = self.session.get('session_key')


        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}


        self.cart = cart



    
    def db_add(self,product , quantity):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass

        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        if self.request.user.is_authenticated:
            obj = Profile.objects.filter(user=self.request.user)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            obj.update(old_cart=str(carty))
            
          

       


    
    def add(self,product , quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            # self.cart[product_id] += quantity 
            pass

        else:
            # item_data = {
            #     'price': str(product.price),
            #     'name': str(product.name),
            #     'category': str(product.category)
            # }
            #self.cart[product_id] = item_data
            # self.cart[product_id] = {'price':str(product.price)} 
            # self.cart[product_id] = {'price':str(product.price),'qty':quantity}

            self.cart[product_id] = int(product_qty)


        if self.request.user.is_authenticated:
            obj = Profile.objects.filter(user=self.request.user)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            obj.update(old_cart=str(carty))
            
          

        self.session.modified = True



    def __len__(self):
        return len(self.cart)
    


    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    

    def cart_total(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        quantities = self.cart

        total = decimal.Decimal('0.00')

        for key,value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * int(value))
                    else:
                        total = total + (product.price * int(value))

        return total
    



    def update(self,product , quantity):
        product_id = str(product)
        product_qty = str(quantity)

        ourcart = self.cart

        ourcart[product_id] = product_qty

        self.session.modified = True

        if self.request.user.is_authenticated:
            obj = Profile.objects.filter(user=self.request.user)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            obj.update(old_cart=str(carty))
       

        thing = self.cart

        return thing
    

    
    def delete(self,product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        if self.request.user.is_authenticated:
            obj = Profile.objects.filter(user=self.request.user)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            obj.update(old_cart=str(carty))
            


        
        
