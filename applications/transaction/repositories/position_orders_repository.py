import logging
import traceback

from applications.transaction.models import PositionOrders
from django.db import transaction


logger = logging.getLogger(__name__)


# 25.02.26 윤택한
# Position 테이블 관리 Repository
class PositionOrdersRepository:
    # 25.02.27(목) 윤택한
    # positions_data 저장
    @staticmethod
    def create(position_orders_data):
        try:
            if not position_orders_data:
                logger.warning("저장할 position_orders_data가 없습니다.")
                return None

            PositionOrders.objects.bulk_create(
                [PositionOrders(**data) for data in position_orders_data],
                ignore_conflicts=True,
            )

            logger.info(f"{len(position_orders_data)}개의 Position 데이터 저장 완료")
            return True

        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"Position 데이터 저장 중 오류 발생: {e}\n{error_trace}")
            return None
