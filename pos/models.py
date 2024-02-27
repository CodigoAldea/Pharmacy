from django.db import models
from medicine.models import Medicine
from accounts.models import Customer
from stocks.models import batch, Stocks
from purchase.models import Purchase_details

class POS(models.Model):
    # Point of Sale (POS) model representing customer orders
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, help_text="Customer placing the order")
    order_no = models.IntegerField(unique=True, help_text="Unique order number for identification")
    order_id = models.ManyToManyField(Medicine, through='Order', help_text="Medicines included in the order")
    date_entry = models.DateField(auto_now=True, editable=True, help_text="Date of order entry")

    def __str__(self):
        return f"{self.customer_id.name} order - {self.order_no}"

class Order(models.Model):
    # Order model representing individual items in a customer order
    medicine_name = models.ForeignKey(Medicine, on_delete=models.CASCADE, help_text="Medicine included in the order")
    customer = models.ForeignKey('POS', verbose_name=("Order_id"), on_delete=models.CASCADE, help_text="Order to which the item belongs")
    quantity = models.IntegerField(help_text="Quantity of the medicine in the order")
    unit = models.CharField(max_length=30, help_text="Unit of measurement for the quantity")
    batch_id = models.ForeignKey(batch, on_delete=models.CASCADE, help_text="Batch of the medicine")

    def __str__(self):
        return self.medicine_name.name

    @property
    def order_number(self):
        return self.customer.order_no

    def price_per(self):
        # Calculate the price per unit of the ordered medicine
        unit=self.unit
        purchase = Purchase_details.objects.filter(medicine_name=self.medicine_name, batch_id=self.batch_id).last()
        if purchase:
            if unit=='box':
                return purchase.box_sp
            elif unit=='strip':
                return purchase.strip_sp
            elif unit=='piece':
                return purchase.tabs_sp
            # return round((purchase.box_sp / (purchase.tabs_strip * purchase.box_size)), 2)

    def total_price(self):
        # Calculate the total price for the ordered quantity
        purchase = Purchase_details.objects.filter(medicine_name=self.medicine_name, batch_id=self.batch_id).last()
        if purchase:
            unit=self.unit
            if unit=='box':
                return purchase.box_sp*self.quantity
            elif unit=='strip':
                return purchase.strip_sp*self.quantity
            elif unit=='piece':
                return purchase.tabs_sp*self.quantity
            # return round((purchase.box_sp / (purchase.tabs_strip * purchase.box_size)) * self.quantity, 2)

class Invoice(models.Model):
    # Invoice model representing customer invoices
    pos_order = models.OneToOneField(POS, on_delete=models.CASCADE, help_text="POS order associated with the invoice")
    payment_method=models.CharField(("Payment Method"), max_length=50,null=True,blank=True)
    date_entry=models.DateField(auto_now_add=True, editable=True, help_text="Date of invoice entry", null=True, blank=True)

    def Total_Price(self):
        # Calculate the total price of all items in the invoice
        orders = Order.objects.filter(customer=self.pos_order)
        order_total_sum = sum(order.total_price() for order in orders)
        return order_total_sum

    def med_name(self):
        # Get the names of medicines in the invoice
        orders = Order.objects.filter(customer=self.pos_order)
        return [j.medicine_name.name for j in orders]

    def order_items(self):
        # Get the quantities of medicines in the invoice
        orders = Order.objects.filter(customer=self.pos_order)
        return [j.quantity for j in orders]

    def order_unit(self):
        # Get the units of medicines in the invoice
        orders = Order.objects.filter(customer=self.pos_order)
        return [j.unit for j in orders]

    def items_price(self):
        # Get the price per unit for each medicine in the invoice
        orders = Order.objects.filter(customer=self.pos_order)
        return [i.price_per() for i in orders]

    def items_expiry(self):
        # Get the expiry dates for each medicine in the invoice
        orders = Order.objects.filter(customer=self.pos_order)
        exp_date=[(i.batch_id.expiry.strftime('%Y-%m-%d')) for i in orders]
        return(exp_date)

    def uni_id(self):
        return f'{self.pos_order.order_no}-Pharma_cust'

    def __str__(self):
        return f'{self.pos_order.order_no}-Pharma_cust'

class Return(models.Model):
    # Return model representing returned items
    invoice_no = models.ForeignKey(Invoice, on_delete=models.CASCADE, help_text="Invoice associated with the returned items")
    date = models.DateField(auto_now=False, auto_now_add=True, help_text="Date of return")

    def __str__(self):
        return str(self.invoice_no)

class ReturnDetails(models.Model):
    # ReturnDetails model representing details of returned items
    inv_number = models.ForeignKey("Return", verbose_name=("invoice number"), on_delete=models.CASCADE, help_text="Return associated with the invoice")
    returned_item = models.ForeignKey(Medicine, on_delete=models.CASCADE, help_text="Medicine returned")
    batch_id = models.ForeignKey(batch, on_delete=models.CASCADE, help_text="Batch of the returned medicine")
    quantity = models.IntegerField(help_text="Quantity of the returned medicine")
    unit=models.CharField(max_length=50)
    date=models.DateField(auto_now=False, auto_now_add=True, help_text="Date of return")
    
    @property
    def cust_phone(self):
        return self.inv_number.invoice_no.pos_order.customer.phone

    def order_items(self):
        # Get the order details for returned items
        order = Order.objects.filter(customer=(self.inv_number).invoice_no.pos_order)
        return [i for i in order]
    @property
    def order_items_price(self):
        # Get the price per unit for each returned item
        price=Order.objects.filter(customer=(self.inv_number).invoice_no.pos_order,medicine_name=self.returned_item)
        return [(i.price_per()) for i in price][0]
    @property
    def total_price_order(self):
        price=Order.objects.filter(customer=(self.inv_number).invoice_no.pos_order,medicine_name=self.returned_item)
        return [(i.price_per())*self.quantity for i in price][0]
class ReturnPurchase(models.Model):
    # ReturnPurchase model representing returned purchases
    medicine_name=models.CharField( max_length=150)
    supplier_name=models.CharField( max_length=150)
    quantity=models.IntegerField(help_text="Quantity of the returned medicine")
    unit=models.CharField(max_length=50)
    last_purchase_id=models.CharField( max_length=50)
    batch_id=models.ForeignKey(batch, on_delete=models.CASCADE, help_text="Batch of the returned medicine")
    date = models.DateField(auto_now=False, auto_now_add=True, help_text="Date of return")

    def __str__(self):
        return str(self.medicine_name)+' - '+str(self.batch_id)
