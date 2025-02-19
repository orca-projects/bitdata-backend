from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.
# class User(AbstractUser):
#     email = models.EmailField(max_length=255, unique=True)
#     username = models.CharField(max_length=150)
#     phone = models.CharField(max_length=30, null=True, blank=True)
#     gender = models.CharField(max_length=10, null=True, blank=True)
#     nickname = models.CharField(max_length=20, null=True, blank=True)
#     # fullname = models.CharField(max_length=20, null=True, blank=True)
#     # kakaoid = models.BigIntegerField(null=True, blank=True)

#     USERNAME_FIELD = "email"  # 사용자의 고유한 식별자로 사용되는 필드
#     REQUIRED_FIELDS = ["username"]  # 슈퍼유저를 생성할 때 프롬프트되는 추가 필드 목록

#     def __str__(self):
#         return f"{self.email} - {self.username}"


# 만들어진 유저 카카오테이블 가져와서 생성
class User(models.Model):
    id = models.AutoField(primary_key=True)  # serial은 AutoField에 매핑
    kakao_id = models.BigIntegerField(
        unique=True, db_column="kakaoId"
    )  # UUID 대신 BigIntegerField
    account_email = models.EmailField(
        max_length=255, db_column="accountEmail"
    )  # varchar(255)와 이메일 제약 조건
    name = models.CharField(max_length=255)  # varchar(255)
    phone_number = models.CharField(
        max_length=255, db_column="phoneNumber"
    )  # varchar(255)
    created_at = models.DateTimeField(
        auto_now_add=True, db_column="createdAt"
    )  # timestamp default now()
    deleted_at = models.DateTimeField(
        null=True, blank=True, db_column="deletedAt"
    )  # nullable timestamp

    class Meta:
        db_table = "User"  # 기존 테이블 이름 매핑
        managed = False  # Django가 이 테이블을 관리하지 않음 (기존 테이블이므로)

    def __str__(self):
        return f"{self.account_email} - {self.name}"


class UserKeyInfo(models.Model):
    id = models.AutoField(primary_key=True)  # serial은 AutoField에 매핑
    kakao_id = models.ForeignKey(
        "User",  # User 모델과 외래 키로 연결
        to_field="kakao_id",  # 외래 키가 kakao_id임을 명시
        db_column="kakaoId",  # 데이터베이스 컬럼 이름 매핑
        on_delete=models.CASCADE,  # 부모(User) 삭제 시 동작 정의
    )
    binance_id = models.CharField(max_length=255, db_column="binanceId")  # varchar(255)
    created_at = models.DateTimeField(
        default=timezone.now, db_column="createdAt"
    )  # timestamp default now()
    is_connected = models.BooleanField(db_column="isConnected", default=False)
    is_key_active = models.BooleanField(db_column="isKeyActive", default=True)
    binance_api_key = models.CharField(
        max_length=255, db_column="binanceApiKey"
    )  # varchar(255)
    binance_secret_key = models.CharField(
        max_length=255, db_column="binanceSecretKey"
    )  # varchar(255)
    last_collected = models.DateTimeField(null=True, blank=True, db_column="lastCollected")  # 추가된 컬럼

    class Meta:
        db_table = "UserKeyInfo"  # 기존 테이블 이름 매핑
        managed = False  # Django가 이 테이블을 관리하지 않음 (기존 테이블이므로)

    def __str__(self):
        return f"Binance ID: {self.binance_id}, Key Active: {self.is_key_active}"


# class Orders(models.Model):
#     id = models.AutoField(primary_key=True)
#     binance_id = models.ForeignKey(
#         "UserKeyInfo",
#         db_column="binanceId",
#         on_delete=models.CASCADE,
#     )
#     avg_price = models.CharField(max_length=255, db_column="avgPrice")
#     client_order_id = models.CharField(max_length=255, db_column="clientOrderId")
#     cum_quote = models.CharField(max_length=255, db_column="cumQuote")
#     executed_qty = models.CharField(max_length=255, db_column="executedQty")
#     order_id = models.CharField(max_length=255, db_column="orderId")
#     orig_qty = models.CharField(max_length=255, db_column="origQty")
#     orig_type = models.CharField(max_length=255, db_column="origType")
#     price = models.CharField(max_length=255, db_column="price")
#     reduce_only = models.BooleanField(default=False, db_column="reduceOnly")
#     side = models.CharField(max_length=255, db_column="side")
#     position_side = models.CharField(max_length=255, db_column="positionSide")
#     status = models.CharField(max_length=255, db_column="status")
#     stop_price = models.CharField(max_length=255, null=True, blank=True, db_column="stopPrice")
#     close_position = models.BooleanField(default=False, db_column="closePosition")
#     symbol = models.CharField(max_length=255, db_column="symbol")
#     time = models.BigIntegerField(db_column="time")
#     time_in_force = models.CharField(max_length=255, db_column="timeInForce")
#     type = models.CharField(max_length=255, db_column="type")
#     update_time = models.BigIntegerField(db_column="updateTime")
#     working_type = models.CharField(max_length=255, db_column="workingType")
#     price_protect = models.BooleanField(default=False, db_column="priceProtect")
#     price_match = models.CharField(max_length=255, default="NONE", db_column="priceMatch")
#     self_trade_prevention_mode = models.CharField(max_length=255, default="NONE", db_column="selfTradePreventionMode")
#     created_at = models.DateTimeField(default=timezone.now, db_column="createdAt")

#     class Meta:
#         db_table = "Orders"
#         managed = False

#     def __str__(self):
#         return f"Order ID: {self.order_id}, Symbol: {self.symbol}"
class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    binance_id = models.ForeignKey(
        "UserKeyInfo",
        db_column="binanceId",
        on_delete=models.CASCADE,
    )
    avg_price = models.CharField(max_length=255, db_column="avgPrice")
    client_order_id = models.CharField(max_length=255, db_column="clientOrderId")
    cum_quote = models.CharField(max_length=255, default="0", db_column="cumQuote")
    executed_qty = models.CharField(max_length=255, db_column="executedQty")
    order_id = models.CharField(max_length=255, db_column="orderId")
    orig_qty = models.CharField(max_length=255, db_column="origQty")
    orig_type = models.CharField(max_length=255, db_column="origType")
    price = models.CharField(max_length=255, db_column="price")
    reduce_only = models.BooleanField(default=False, db_column="reduceOnly")
    side = models.CharField(max_length=255, db_column="side")
    position_side = models.CharField(max_length=255, db_column="positionSide")
    status = models.CharField(max_length=255, db_column="status")
    stop_price = models.CharField(max_length=255, null=True, blank=True, db_column="stopPrice")
    close_position = models.BooleanField(default=False, db_column="closePosition")
    symbol = models.CharField(max_length=255, db_column="symbol")
    time = models.BigIntegerField(db_column="time")
    time_in_force = models.CharField(max_length=255, db_column="timeInForce")
    type = models.CharField(max_length=255, db_column="type")
    update_time = models.BigIntegerField(db_column="updateTime")
    working_type = models.CharField(max_length=255, db_column="workingType")
    price_protect = models.BooleanField(default=False, db_column="priceProtect")
    price_match = models.CharField(max_length=255, default="NONE", db_column="priceMatch")
    self_trade_prevention_mode = models.CharField(max_length=255, default="NONE", db_column="selfTradePreventionMode")
    good_till_date = models.BigIntegerField(default=0, db_column="goodTillDate")
    created_at = models.DateTimeField(default=timezone.now, db_column="createdAt")
    class Meta:
        db_table = "Orders"
        managed = False

    def __str__(self):
        return f"Order ID: {self.order_id}, Symbol: {self.symbol}"

    

class Positions(models.Model):
    id = models.AutoField(primary_key=True)
    binance_id = models.ForeignKey(
        "UserKeyInfo",
        db_column="binanceId",
        on_delete=models.CASCADE,
    )
    order_id = models.CharField(max_length=255, db_column="orderId")
    created_at = models.DateTimeField(default=timezone.now, db_column="createdAt")

    class Meta:
        db_table = "Positions"
        managed = False

    def __str__(self):
        return f"Position Order ID: {self.order_id}"


class Trades(models.Model):
    id = models.AutoField(primary_key=True)
    binance_id = models.ForeignKey(
        "UserKeyInfo",
        db_column="binanceId",
        on_delete=models.CASCADE,
    )
    buyer = models.BooleanField(db_column="buyer")
    commission = models.CharField(max_length=255, db_column="commission")
    commission_asset = models.CharField(max_length=255, db_column="commissionAsset")
    trade_id = models.CharField(max_length=255, db_column="tradeId")
    maker = models.BooleanField(db_column="maker")
    order_id = models.CharField(max_length=255, db_column="orderId")
    price = models.CharField(max_length=255, db_column="price")
    qty = models.CharField(max_length=255, db_column="qty")
    quote_qty = models.CharField(max_length=255, db_column="quoteQty")
    realized_pnl = models.CharField(max_length=255, db_column="realizedPnl")
    side = models.CharField(max_length=255, db_column="side")
    position_side = models.CharField(max_length=255, db_column="positionSide")
    symbol = models.CharField(max_length=255, db_column="symbol")
    time = models.BigIntegerField(db_column="time")
    created_at = models.DateTimeField(default=timezone.now, db_column="createdAt")

    class Meta:
        db_table = "Trades"
        managed = False

    def __str__(self):
        return f"Trade ID: {self.trade_id}, Symbol: {self.symbol}"
    

class Transactions(models.Model):
    id = models.AutoField(primary_key=True)
    binance_id = models.ForeignKey(
        "UserKeyInfo",
        db_column="binanceId",
        on_delete=models.CASCADE,
    )
    symbol = models.CharField(max_length=255, db_column="symbol")
    income_type = models.CharField(max_length=255, db_column="incomeType")
    income = models.CharField(max_length=255, db_column="income")
    asset = models.CharField(max_length=255, db_column="asset")
    info = models.CharField(max_length=255, db_column="info")
    time = models.BigIntegerField(db_column="time")
    tran_id = models.CharField(max_length=255, db_column="tranId")
    trade_id = models.CharField(max_length=255, db_column="tradeId")
    created_at = models.DateTimeField(default=timezone.now, db_column="createdAt")

    class Meta:
        db_table = "Transactions"
        managed = False

    def __str__(self):
        return f"Transaction ID: {self.tran_id}, Asset: {self.asset}"