from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_route('notify', '/notify')
    config.add_route('fb_register_notify', '/notify/fb/register')
    config.add_route('fb_sell_notify', '/notify/fb/sell')
    config.add_route('page_product_notify', '/notify/page/product')
    config.add_route('page_company_notify', '/notify/page/company')
    config.add_route('page_demand_notify', '/notify/page/demand')
    config.add_route('fb_newcompany_notify', '/notify/fb/newcompany')
    config.scan()
    return config.make_wsgi_app()

