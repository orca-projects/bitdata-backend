from django.utils import timezone
from datetime import datetime as dt_type, timezone as dt_timezone


class DateUtil:
    @staticmethod
    def parse_timestamp_to_datetime(timestamp) -> timezone.datetime:
        if isinstance(timestamp, str):
            timestamp = int(timestamp)
        elif not isinstance(timestamp, (int, float)):
            raise ValueError("timestamp는 int, float 또는 str 타입이어야 합니다.")

        return timezone.make_aware(
            timezone.datetime.fromtimestamp(timestamp / 1000), dt_timezone.utc
        )

    @staticmethod
    def parse_datetime_to_timestamp(datetime_obj) -> int:
        if isinstance(datetime_obj, str):
            try:
                datetime_obj = dt_type.fromisoformat(datetime_obj)
                datetime_obj = timezone.make_aware(datetime_obj, dt_timezone.utc)
            except Exception as e:
                raise ValueError(
                    f"datetime 문자열 포맷이 잘못되었습니다: {datetime_obj}"
                ) from e

        if not isinstance(datetime_obj, dt_type):
            raise ValueError("datetime_obj는 datetime 또는 ISO 포맷 str이어야 합니다.")

        if timezone.is_naive(datetime_obj):
            datetime_obj = timezone.make_aware(datetime_obj, dt_timezone.utc)

        return int(datetime_obj.timestamp() * 1000)
