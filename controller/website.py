from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.tools import lazy
from odoo.addons.website_sale.controllers.main import TableCompute
from datetime import datetime


class WebsiteSaleInherit(WebsiteSale):
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        record = super(WebsiteSaleInherit, self).shop(page=0, category=None, search='', min_price=0.0, max_price=0.0,
                                                      ppg=False, **post)
        products = request.env.user.allowed_products_ids
        category = request.env.user.categories_id
        if products or category:
            if category:
                category = category.search([('id', '=', int(category))], limit=1)
            website = request.env['website'].get_current_website()
            website_domain = website.website_domain()
            if ppg:
                try:
                    ppg = int(ppg)
                    post['ppg'] = ppg
                except ValueError:
                    ppg = False
            if not ppg:
                ppg = website.shop_ppg or 20

            ppr = website.shop_ppr or 4

            pricelist = website.pricelist_id

            categs_domain = [('parent_id', '=', False)] + website_domain
            if search:
                search_categories = category.search(
                    [('product_tmpl_ids', 'in', products.ids)] + website_domain
                ).parents_and_self
                categs_domain.append(('id', 'in', search_categories))
            else:
                search_categories = category
            categs = lazy(lambda: category.search(categs_domain))

            fiscal_position_sudo = website.fiscal_position_id.sudo()
            products_prices = lazy(lambda: products._get_sales_prices(pricelist, fiscal_position_sudo))

            record.qcontext.update({
                'category': category,
                'pricelist': pricelist,
                'fiscal_position': fiscal_position_sudo,
                'products': products,
                'bins': lazy(lambda: TableCompute().process(products, ppg, ppr)),
                'ppg': ppg,
                'ppr': ppr,
                'categories': categs,
                'products_prices': products_prices,
                'get_product_prices': lambda product: lazy(lambda: products_prices[product.id]),
            })
        return record
