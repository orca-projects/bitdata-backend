import logging
import traceback

from applications.users.models import Orders


logger = logging.getLogger(__name__)


# 25.02.18 윤택한
# Orders 테이블 관리 Repository
class OrdersRepository:
    @staticmethod
    def get_last_order_id():
        try:
            last_order = Orders.objects.order_by("-order_id").first()
            return last_order.order_id if last_order else 0  # 데이터가 없으면 0 반환
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"마지막 Orders ID 조회 중 오류 발생: {e}\n{error_trace}")
            return 0  # 오류 발생 시 기본값 0 반환

    # 25.02.18 윤택한
    # orders data 저장
    @staticmethod
    def save_orders_data(binance_id, orders_data):
        try:
            if not orders_data:
                logger.warning("주문 데이터 없음")
                return None

            orders_objects = [
                Orders(binance_id=binance_id, **order) for order in orders_data
            ]

            Orders.objects.bulk_create(orders_objects)
            logger.info(f"{len(orders_objects)}개의 Orders 데이터를 저장했습니다.")

        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"Orders 데이터 저장 중 오류 발생: {e}\n{error_trace}")
            raise RuntimeError("Orders 데이터 저장 중 오류 발생")

    # 25.02.28(금) 윤택한
    # orders_datas 가져오기
    @staticmethod
    def get_order_by_order_id(order_id):
        try:
            return Orders.objects.get(order_id=order_id)
        except Orders.DoesNotExist:
            error_trace = traceback.format_exc()
            logger.error(
                f"Order ID {order_id}에 대한 Orders 데이터가 존재하지 않습니다.\n{error_trace}"
            )
            return None
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"Orders 데이터 조회 중 오류 발생: {e}\n{error_trace}")
            return None

    @staticmethod
    def get_orders_by_order_ids(order_ids):
        try:
            return Orders.objects.filter(order_id__in=order_ids).order_by("time")
        except Exception as e:
            logger.error(f"Orders 데이터 조회 중 오류 발생: {e}")
            return None
