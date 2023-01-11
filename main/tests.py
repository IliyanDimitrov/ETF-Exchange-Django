from decimal import Decimal
from django.test import TestCase, TransactionTestCase
from .models import Order, Balance, PortfolioPnL
from django.contrib.auth.models import User


class OrderModelTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

        # Create an order
        self.order = Order.objects.create(
            ticker='TEST',
            name='Test Order',
            price=Decimal('10.50'),
            quantity=2,
            type='BUY',
            user=self.user
        )

    def test_create_order(self):
        # Check that the order was created in the database
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().ticker, 'TEST')

    def test_string_representation(self):
        # Check that the string representation of the order is as expected
        self.assertEqual(str(self.order), 'TEST - Test Order - 10.50 - 2')

    def test_total_property(self):
        # Check that the total property of the order is calculated correctly
        self.assertEqual(self.order.total, Decimal('21.00'))

class OrderModelIntegrationTestCase(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.order = Order.objects.create(
            ticker='TEST',
            name='Test Order',
            price=Decimal('10.50'),
            quantity=2,
            type='BUY',
            user=self.user
        )

    def test_fulfilled_field(self):
        """Tests that the fulfilled field can be updated and saved to the database."""
        self.order.fulfilled = True
        self.order.save()
        self.assertEqual(Order.objects.get(pk=self.order.pk).fulfilled, True)


class BalanceModelTest(TestCase):
    def test_string_representation(self):
        # Create a balance with some test data
        balance = Balance(ticker='AAPL', name='Apple Inc.', buy_price=Decimal('10.50'), quantity=10)

        # Check that the string representation of the balance is as expected
        self.assertEqual(str(balance), 'AAPL - Apple Inc. - 10.50 - 10')


class BalanceModelIntegrationTest(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.balance = Balance.objects.create(
            ticker='AAPL',
            name='Apple Inc.',
            buy_price=10.50,
            quantity=10,
            user=self.user
        )
    
    def test_update_quantity(self):
        """Tests that the quantity field can be updated and saved to the database."""
        self.balance.quantity = 15
        self.balance.save()
        self.assertEqual(Balance.objects.get(pk=self.balance.pk).quantity, 15)
    
    def test_update_price(self):
        """Tests that the price field can be updated and saved to the database."""
        self.balance.buy_price = 12.50
        self.balance.save()
        self.assertEqual(Balance.objects.get(pk=self.balance.pk).buy_price, 12.50)
    
    def test_create_balance(self):
        """Tests that a new balance can be created and saved to the database."""
        balance = Balance.objects.create(
            ticker='GOOG',
            name='Google Inc.',
            buy_price=1000.00,
            quantity=1,
            user=self.user
        )
        self.assertEqual(Balance.objects.count(), 2)
        self.assertEqual(Balance.objects.last().ticker, 'GOOG')


class PortfolioPnLModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.portfolio_pnl = PortfolioPnL.objects.create(
            user=self.user,
            pnl=Decimal('100.00'),
            principal=Decimal('200.00')
        )

    def test_create_portfolio_pnl(self):
        self.assertEqual(PortfolioPnL.objects.count(), 1)
        self.assertEqual(PortfolioPnL.objects.first().pnl, Decimal('100.00'))
        self.assertEqual(PortfolioPnL.objects.first().principal, Decimal('200.00'))
        