import logging
from django.utils import timezone

from applications.users.models import UserBinance


logger = logging.getLogger(__name__)


class UserBinanceRepository:
    @staticmethod
    def get_binance_uid_by_id(user_binance_id):
        try:
            user_binance = UserBinance.objects.get(id=user_binance_id)
            return user_binance.binance_uid
        except UserBinance.DoesNotExist:
            logger.warning(f"UserBinance ID {user_binance_id}가 존재하지 않습니다.")
            return None
        except Exception as e:
            logger.exception("UserBinance 조회 중 오류 발생")
            raise e

    @staticmethod
    def set_user_binance(binance_uid):
        try:
            user_binance, created = UserBinance.objects.get_or_create(
                binance_uid=binance_uid,
                defaults={
                    "updated_at": timezone.now(),
                    "last_collected": timezone.now(),
                },
            )
            if not created:
                user_binance.updated_at = timezone.now()
                user_binance.last_collected = timezone.now()
                user_binance.save(update_fields=["updated_at", "last_collected"])
            return user_binance
        except Exception as e:
            logger.exception("UserBinance 처리 중 오류 발생")
            raise e
