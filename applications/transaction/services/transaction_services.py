from django.db import transaction

from applications.transaction.models import PositionHistory, PositionOrders


class TransactionServices:
    @staticmethod
    def save_position(position_dto_lsit):
        with transaction.atomic():
            for position_dto in position_dto_lsit:
                position_history_obj = PositionHistory.objects.create(
                    **position_dto.to_position_history_data()
                )

                position_order_data = position_dto.to_position_order_data(
                    position_history_obj.id
                )
                PositionOrders.objects.bulk_create(
                    [PositionOrders(**order_data) for order_data in position_order_data]
                )
