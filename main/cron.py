from django.core.management.base import BaseCommand
from .tiingo import get_price_data
from .models import Balance, PortfolioPnL
from decimal import Decimal
from django.contrib.auth.models import User
from django_cron import CronJobBase, Schedule
import logging


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440 # once a day 
    RETRY_AFTER_FAILURE_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'main.my_cron_job'    # a unique code
    logger = logging.getLogger(__name__)

    def do(self):
        self.logger.debug("Cron job running!") 
        users = User.objects.all()
        # Calculate and save the PnL for each user's portfolio
        for user in users:
            balances = Balance.objects.filter(user=user)
            total_pnl = 0
            principal = 0
            try:
                for balance in balances:
                    current_price = get_price_data(balance.ticker)
                    balance.current_price = round(Decimal(current_price['close']), 2)
                    balance.pnl = (balance.current_price - balance.buy_price) * balance.quantity
                    total_pnl += balance.pnl
                    principal += balance.buy_price * balance.quantity
                portfolio_pnl, created = PortfolioPnL.objects.get_or_create(user=user, defaults={'pnl': total_pnl, 'principal': principal})
                balance.save()
                portfolio_pnl.save()
            except Exception as e:
                self.logger.exception("Error while processing user: {}. Error: {}".format(user, e))