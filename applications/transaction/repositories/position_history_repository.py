import logging
import traceback

from applications.transaction.models import PositionHistory


logger = logging.getLogger(__name__)


class PositionHistoryRepository:
    @staticmethod
    def get_last_closed_at(binance_id):
        try:
            last_position = (
                PositionHistory.objects.filter(binance_id=binance_id)
                .order_by("-position_closed_at")
                .first()
            )

            return last_position.position_closed_at if last_position else 0
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(
                f"마지막 포지션 종료 시간 조회 중 오류 발생: {e}\n{error_trace}"
            )
            return 0

    @staticmethod
    def get_position_by_date(binance_id, start_date, end_date):
        try:
            positions = PositionHistory.objects.filter(
                binance_id=binance_id,
                position_closed_at__gte=start_date,
                position_closed_at__lte=end_date,
            ).order_by("-position_closed_at")
            return positions
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"포지션 기간 조회 중 오류 발생: {e}\n{error_trace}")
            return PositionHistory.objects.none()
