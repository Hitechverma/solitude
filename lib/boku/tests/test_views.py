import json
import uuid
from django.core.urlresolvers import reverse
from nose.tools import eq_

from lib.sellers.models import Seller, SellerBoku
from .utils import SellerBokuTest


class TestSellerBokuViews(SellerBokuTest):

    def test_list_view_lists_all_sellers(self):
        for i in range(3):
            seller = Seller.objects.create(uuid=str(uuid.uuid4()))
            SellerBoku.objects.create(
                seller=seller,
                merchant_id=self.example_merchant_id,
                service_id=self.example_service_id,
            )

        response = self.client.get(reverse('sellerboku-list'))
        eq_(response.status_code, 200, response.content)
        sellers_data = json.loads(response.content)
        eq_(len(sellers_data['objects']), 3)

    def test_create_view_creates_seller_boku(self):
        response = self.client.post(
            reverse('sellerboku-list'), data=self.seller_data
        )
        eq_(response.status_code, 201, response.content)
        seller_boku_data = json.loads(response.content)

        seller_boku = SellerBoku.objects.get(pk=seller_boku_data['id'])
        eq_(seller_boku.seller, self.seller)
        eq_(seller_boku.merchant_id, self.seller_data['merchant_id'])
        eq_(seller_boku.service_id, self.seller_data['service_id'])

    def test_detail_view_returns_seller_boku(self):
        test_domain = 'test.com'
        seller_boku = SellerBoku.objects.create(
            seller=self.seller,
            merchant_id=self.example_merchant_id,
            service_id=self.example_service_id,
        )
        response = self.client.get(
            reverse('sellerboku-detail', kwargs={'pk': seller_boku.pk}),
            SERVER_NAME=test_domain
        )
        eq_(response.status_code, 200, response.content)

        seller_boku_data = json.loads(response.content)
        eq_(seller_boku_data['id'], seller_boku.pk)
        eq_(seller_boku_data['seller'], self.seller_uri)
        eq_(seller_boku_data['merchant_id'], seller_boku.merchant_id)
        eq_(seller_boku_data['service_id'], seller_boku.service_id)
        eq_(
            seller_boku_data['resource_uri'],
            'http://{domain}{path}'.format(
                domain=test_domain,
                path=reverse(
                    'sellerboku-detail',
                    kwargs={'pk': seller_boku.pk}
                )
            )
        )

    def test_update_view_modifies_existing_seller_boku(self):
        new_merchant_id = '54321'
        seller_boku = SellerBoku.objects.create(
            seller=self.seller,
            merchant_id=self.example_merchant_id,
            service_id=self.example_service_id,
        )
        response = self.client.patch(
            reverse('sellerboku-detail', kwargs={'pk': seller_boku.pk}),
            data={'merchant_id': new_merchant_id},
        )
        eq_(response.status_code, 200, response.content)

        seller_boku = SellerBoku.objects.get(pk=seller_boku.pk)
        eq_(seller_boku.merchant_id, new_merchant_id)

    def test_delete_not_allowed(self):
        seller_boku = SellerBoku.objects.create(
            seller=self.seller,
            merchant_id=self.example_merchant_id,
            service_id=self.example_service_id,
        )
        response = self.client.delete(
            reverse('sellerboku-detail', kwargs={'pk': seller_boku.pk})
        )
        eq_(response.status_code, 403, response.content)