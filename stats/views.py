from importlib.resources.readers import remove_duplicates
from itertools import product
from symtable import Class
from django.db .models import Q

from django.db.models.fields import return_None
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.context_processors import request
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages

from main.models import Product, Cliend
from .models import Sale, ImportProduct, Pay_debt
from .models import Pay_debt



class SalesView(LoginRequiredMixin, View):
    login_url = 'login'



    def get(self, request):
        global salesl
        sales = Sale.objects.filter(branch=request.user.branch).order_by('-created_at')
        products = Product.objects.filter(branch=request.user.branch).order_by('name')
        clients = Cliend.objects.filter(branch=request.user.branch).order_by('name')

        search = request.GET.get('search')
        if search:
            salesl = sales.filter(
                Q(product__name__icontains=search) |
                Q(cliend__name__icontains=search)

            )
        context={
            'sales': sales,
            'products': products,
            'clients': clients,
            'search': search
        }

        return render(request, 'sales.html', context)

    def post(self, request):
        product = get_object_or_404(Product, id=request.POST['product_id'])
        cliend = get_object_or_404(Cliend, id=request.POST['cliend_id'])

        quantity = float(request.POST.get('quantity')) if request.POST.get('quantity') is not None else None
        total_price = float(request.POST.get('total_price')) if request.POST.get('total_price') is not None else None
        paid = float(request.POST.get('paid_price')) if request.POST.get('paid_price') is not None else None
        debt = float(request.POST.get('debt_price')) if request.POST.get('debt_price') is not None else None

        # CHECK PRODUCT QUANTITY
        context = self.check_enough_product(product, quantity)
        if context is not None:
            return render(request, 'warning.html', context)

        # debt and paid not None
        if debt and paid:
            total_price = debt + paid

        # calculate total_price
        if not total_price:
            total_price = product.price * quantity

        # paid and debt is None
        if not paid  and not debt:
            paid = total_price

        # debt is None
        if not debt and paid:
            debt = total_price - paid

        # paid is None
        if not  paid and debt:
            paid = total_price - debt



        Sale.objects.create(
            product=product,
            cliend=cliend,
            quantity=quantity,
            total_price=total_price,
            paid_price=paid,
            debt_price=debt,
            user=request.user,
            branch=request.user.branch
        )

        # SUB PRODUCT QUANTITY
        product.quantity -= quantity
        product.save()

        # add product debt
        cliend.debt += debt
        cliend.save()



        return redirect('sales')

    def check_enough_product(self, product, quantity):
        if product.quantity < quantity:
            warning_massage = f"{product.name} so'ralgan miqdorda mavjud emas! Mavjud: {product.quantity} {product.unit}"
            warning_title = "Mahsulot yetarli emas!"
            back_url = 'sales'
            context = {
                'warning_massage': warning_massage,
                'warning_title': warning_title,
                'back_url': back_url
            }
            return context
        return None

class ImportProductsView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        import_products = ImportProduct.objects.filter(branch=request.user.branch).order_by('-created_at')
        products = Product.objects.filter(branch=request.user.branch).order_by('name')
        search = request.GET.get('search')
        if search:
            i_products = import_products.filter(
                Q(product__name__icontains=search)
            )
        context={
            'import_products': import_products,
            'products': products,
            'search': search
        }
        return render(request,'import-products.html', context)

    def post(self, request):
        product = get_object_or_404(Product, id=request.POST['product_id'])
        quantity = float(request.POST.get('quantity')) if request.POST.get('quantity') is not None else None
        ImportProduct.objects.create(
            product=product,
            quantity=quantity,
            buy_price=request.POST.get('buy_price'),
            user=request.user,
            branch=request.user.branch
        )
        product.quantity += quantity
        product.save()
        return redirect('imports')

class ImportProducEditView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        import_product = get_object_or_404(ImportProduct, pk=pk)


        return render(request, 'import-product-edit.html', {'import_product': import_product})

    def post(self, request, pk):
        import_product = get_object_or_404(ImportProduct, pk=pk)

        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        buy_price = request.POST.get('buy_price')

        product = get_object_or_404(Product, pk=int(product_id))

        import_product.product_id = product
        import_product.quantity = float(quantity)
        import_product.buy_price = float(buy_price)
        import_product.save()

        return redirect('imports')


class PayDebtsView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        pay_debts = Pay_debt.objects.filter(branch=request.user.branch).order_by('-created_at')
        cliends = Cliend.objects.filter(branch=request.user.branch).order_by('name')
        search = request.GET.get('search')
        if search:
            paydebts = pay_debts.filter(
                Q(pay_debts__cliend__name__icontains=search)
            )

        context={
            'pay_debts': pay_debts,
            'cliends': cliends,
            'search': search
        }
        return render(request, 'pay-debts.html', context)
    def post(self, request):
        cliend = get_object_or_404(Cliend, id=request.POST.get('cliend_id'))
        price = float(request.POST.get('price')) if request.POST.get('price') is not None else None
        if price == 0:
            return redirect('pay-debts')
        if price > cliend.debt:
            messages.warning(request, f"{cliend.name}ning qarzi {cliend.debt} so'm. Siz kiritgan summa qarzdan katta!")
            return redirect('pay-debts')

        Pay_debt.objects.create(
            cliend=cliend,
            price=price,
            description=request.POST.get('description'),
            user=request.user,
            branch=request.user.branch
        )

        cliend.debt -= price
        cliend.save()
        return redirect('pay-debts')

def edit_pay_debt(request, pk):
    pay_debt = get_object_or_404(Pay_debt, id=pk)
    cliend = pay_debt.cliend #

    if request.method == "POST":
        new_price = float(request.POST.get('quantity') or 0)
        description = request.POST.get('description')

        if new_price > (cliend.debt + pay_debt.price):
            messages.warning(request,
                             f"{cliend.name}ning qarzi {cliend.debt + pay_debt.price} so'm. Siz kiritgan summa qarzdan katta!")
            return redirect('edit-pay-debt', pk=pay_debt.id)
        cliend.debt = cliend.debt + pay_debt.price - new_price
        cliend.save()

        pay_debt.price = new_price
        pay_debt.description = description
        pay_debt.save()
        messages.success(request, "To‘lov muvaffaqiyatli tahrirlandi!")
        return redirect('pay-debts')

    return render(request, "edit_pay_debt.html", {"pay_debt": pay_debt})
