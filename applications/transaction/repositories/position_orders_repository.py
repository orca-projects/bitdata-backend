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
    def create(positions_data):
        try:
            if not positions_data:
                logger.warning("저장할 positions_data가 없습니다.")
                return None

            position_objects = [
                PositionOrders(
                    binance_uid=data["binanceId"],
                    order_id=data["orderId"],
                    position_id=data["positionId"],
                )
                for data in positions_data
            ]

            with transaction.atomic():  # 트랜잭션 처리 (데이터 일관성 유지)
                PositionOrders.objects.bulk_create(position_objects)

            logger.info(f"{len(positions_data)}개의 Position 데이터 저장 완료")
            return True

        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"Position 데이터 저장 중 오류 발생: {e}\n{error_trace}")
            return None
