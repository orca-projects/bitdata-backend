import logging
import traceback

from django.db.models import Max
from applications.users.models import PositionOrders
from django.db import transaction


logger = logging.getLogger(__name__)


# 25.02.26 윤택한
# Position 테이블 관리 Repository
class PositionOrdersRepository:
    # 25.02.26 윤택한
    # 해당 테이블에서 받아온 binance_id가 가지고 있는 positionId의 최대 값을 return
    @staticmethod
    def get_max_position_id(binance_id):
        try:
            max_position = PositionOrders.objects.filter(
                binance_id=binance_id
            ).aggregate(Max("position_id"))
            max_position_id = max_position.get("position_id__max")

            if max_position_id is None:
                logger.info(f"No positions found for binance_id: {binance_id}")
                return 0  # 기본값 0 반환

            return max_position_id  # int 값 반환

        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"Position ID 조회 중 오류 발생: {e}\n{error_trace}")
            return 0  # 오류 발생 시 기본값 반환

    # 25.02.27(목) 윤택한
    # positions_data 저장
    @staticmethod
    def save_positions_data(positions_data):
        try:
            if not positions_data:
                logger.warning("저장할 positions_data가 없습니다.")
                return None

            position_objects = [
                PositionOrders(
                    binance_id=data["binanceId"],
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

    # 25.02.28(금) 윤택한
    # positions_datas 가져오기
    @staticmethod
    def get_positions(binance_id):
        try:
            return PositionOrders.objects.filter(binance_id=binance_id)
        except Exception as e:
            logger.error(f"포지션 데이터 조회 중 오류 발생: {e}")
            return None
