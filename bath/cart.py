from bath.models import Product


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
        self.all_price = 0

    def add_product(self, product, quantity=0):
        """
        Add a product to the cart
        """
        product_name = product.name
        self.cart[product_name] = {'quantity': quantity,
                                   'price': str(product.price)}
        self.cart[product_name]['quantity'] = quantity
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session['cart'] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
    Перебор элементов в корзине и получение продуктов из базы данных.
    """
        product_names = self.cart.keys()
        products = Product.objects.filter(name__in=product_names)
        for product in products:
            self.cart[str(product.name)]['product'] = product
        for item in self.cart.values():
            quantity = item.get('quantity') or 0
            item['total_price'] = int(item['price']) * int(quantity)
            yield item

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        total = 0
        for product in self.cart:
            total += self.cart[product].get('total_price', 0)
        return total

    def clear(self):
        # удаление корзины из сессии
        del self.session['cart']
        self.session.modified = True
