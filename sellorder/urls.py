from django.urls import path
from . import views

app_name = 'sellorder'

urlpatterns = [

    path('sellorder_list', views.sellorder_list, name='sellorder_list'),
    path('facture_all', views.facture_all, name='facture_all'),

    path('performa_sellorder_list', views.performa_sellorder_list, name='performa_sellorder_list'),
    path('factured_sellorder_list', views.factured_sellorder_list, name='factured_sellorder_list'),

    path('confirm_order_performa/<str:pk>', views.confirm_order_performa, name='confirm_order_performa'),
    path('confirm_order/<str:pk>', views.confirm_order, name='confirm_order'),

    path('sellorder_facture/<str:pk>', views.sellorder_facture, name='sellorder_facture'),
    path('sellorder_facture_pdf/<str:pk>', views.sellorder_facture_pdf, name='sellorder_facture_pdf'),
    path('sellorder_facture_no_date_pdf/<str:pk>', views.sellorder_facture_no_date_pdf, name='sellorder_facture_no_date_pdf'),
    path('sellorder_facture_mo_pdf/<str:pk>', views.sellorder_facture_mo_pdf, name='sellorder_facture_mo_pdf'),
    path('sellorder_facture_mo_no_date_pdf/<str:pk>', views.sellorder_facture_mo_no_date_pdf, name='sellorder_facture_mo_no_date_pdf'),

    # print proforma
    path('sellorder_facture_proforma_pdf/<str:pk>', views.sellorder_facture_proforma_pdf, name='sellorder_facture_proforma_pdf'),
    path('sellorder_facture_proforma_mo_pdf/<str:pk>', views.sellorder_facture_proforma_mo_pdf, name='sellorder_facture_proforma_mo_pdf'),
    path('sellorder_facture_proforma_piece_pdf/<str:pk>', views.sellorder_facture_proforma_piece_pdf, name='sellorder_facture_proforma_piece_pdf'),

    path('bsb_sellorder_facture_proforma_pdf/<str:pk>', views.bsb_sellorder_facture_proforma_pdf, name='bsb_sellorder_facture_proforma_pdf'),
    path('nacer_sellorder_facture_proforma_pdf/<str:pk>', views.nacer_sellorder_facture_proforma_pdf, name='nacer_sellorder_facture_proforma_pdf'),
    path('ghezal_sellorder_facture_proforma_pdf/<str:pk>', views.ghezal_sellorder_facture_proforma_pdf, name='ghezal_sellorder_facture_proforma_pdf'),
    path('sellorder_facture_proforma_pdf_no_date/<str:pk>', views.sellorder_facture_proforma_pdf_no_date, name='sellorder_facture_proforma_pdf_no_date'),

    path('sellorder_list_by_customer/<str:pk>', views.sellorder_list_by_customer,
         name='sellorder_list_by_customer'),
    # print
    path('sellorder_pdf/<str:pk>', views.sellorder_pdf, name='sellorder_pdf'),
    path('sellorder_pour_pdf/<str:pk>', views.sellorder_pour_pdf, name='sellorder_pour_pdf'),
    path('sellorder_livraison_pdf/<str:pk>', views.sellorder_livraison_pdf, name='sellorder_livraison_pdf'),

    path('sellorder_details/<str:pk>', views.sellorder_details, name='sellorder_details'),
    path('sellorder_delete/<str:pk>', views.sellorder_delete, name='sellorder_delete'),
    path('update_order/<str:pk>', views.update_order, name='update_order'),
    path('update_order_performa/<str:pk>', views.update_order_performa, name='update_order_performa'),
    path('order_to_performa/<str:pk>', views.order_to_performa, name='order_to_performa'),

    path('order_item_delete/<str:orderpk>/<str:itempk>', views.order_item_delete, name='order_item_delete'),
    path('confirm_order_item_delete/<str:orderpk>/<str:itempk>', views.confirm_order_item_delete, name='confirm_order_item_delete'),
    path('order_panne_delete/<str:orderpk>/<str:itempk>', views.order_panne_delete, name='order_panne_delete'),
    path('confirm_order_panne_delete/<str:orderpk>/<str:itempk>', views.confirm_order_panne_delete, name='confirm_order_panne_delete'),
    path('confirm_order_service_delete/<str:orderpk>/<str:itempk>', views.confirm_order_service_delete, name='confirm_order_service_delete'),
    path('order_service_delete/<str:orderpk>/<str:itempk>', views.order_service_delete, name='order_service_delete'),

    path('get_orders_pannes', views.get_orders_pannes, name='get_orders_pannes'),
    path('get_orders_pieces', views.get_orders_pieces, name='get_orders_pieces'),
    path('get_orders_pannes_payed', views.get_orders_pannes_payed, name='get_orders_pannes_payed'),
    path('get_orders_pieces_payed', views.get_orders_pieces_payed, name='get_orders_pieces_payed'),

]
