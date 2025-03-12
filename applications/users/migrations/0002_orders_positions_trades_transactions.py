# Generated by Django 5.1.2 on 2025-02-15 16:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Orders",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("avg_price", models.CharField(db_column="avgPrice", max_length=255)),
                (
                    "client_order_id",
                    models.CharField(db_column="clientOrderId", max_length=255),
                ),
                ("cum_base", models.CharField(db_column="cumBase", max_length=255)),
                (
                    "executed_qty",
                    models.CharField(db_column="executedQty", max_length=255),
                ),
                ("order_id", models.CharField(db_column="orderId", max_length=255)),
                ("orig_qty", models.CharField(db_column="origQty", max_length=255)),
                ("orig_type", models.CharField(db_column="origType", max_length=255)),
                ("price", models.CharField(db_column="price", max_length=255)),
                (
                    "reduce_only",
                    models.BooleanField(db_column="reduceOnly", default=False),
                ),
                ("side", models.CharField(db_column="side", max_length=255)),
                (
                    "position_side",
                    models.CharField(db_column="positionSide", max_length=255),
                ),
                ("status", models.CharField(db_column="status", max_length=255)),
                (
                    "stop_price",
                    models.CharField(
                        blank=True, db_column="stopPrice", max_length=255, null=True
                    ),
                ),
                (
                    "close_position",
                    models.BooleanField(db_column="closePosition", default=False),
                ),
                ("symbol", models.CharField(db_column="symbol", max_length=255)),
                ("pair", models.CharField(db_column="pair", max_length=255)),
                ("time", models.BigIntegerField(db_column="time")),
                (
                    "time_in_force",
                    models.CharField(db_column="timeInForce", max_length=255),
                ),
                ("type", models.CharField(db_column="type", max_length=255)),
                (
                    "activate_price",
                    models.CharField(
                        blank=True, db_column="activatePrice", max_length=255, null=True
                    ),
                ),
                (
                    "price_rate",
                    models.CharField(
                        blank=True, db_column="priceRate", max_length=255, null=True
                    ),
                ),
                ("update_time", models.BigIntegerField(db_column="updateTime")),
                (
                    "working_type",
                    models.CharField(db_column="workingType", max_length=255),
                ),
                (
                    "price_protect",
                    models.BooleanField(db_column="priceProtect", default=False),
                ),
                (
                    "price_match",
                    models.CharField(
                        db_column="priceMatch", default="NONE", max_length=255
                    ),
                ),
                (
                    "self_trade_prevention_mode",
                    models.CharField(
                        db_column="selfTradePreventionMode",
                        default="NONE",
                        max_length=255,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        db_column="createdAt", default=django.utils.timezone.now
                    ),
                ),
            ],
            options={
                "db_table": "Orders",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Positions",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("order_id", models.CharField(db_column="orderId", max_length=255)),
                (
                    "created_at",
                    models.DateTimeField(
                        db_column="createdAt", default=django.utils.timezone.now
                    ),
                ),
            ],
            options={
                "db_table": "Positions",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Trades",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("buyer", models.BooleanField(db_column="buyer")),
                (
                    "commission",
                    models.CharField(db_column="commission", max_length=255),
                ),
                (
                    "commission_asset",
                    models.CharField(db_column="commissionAsset", max_length=255),
                ),
                ("trade_id", models.CharField(db_column="tradeId", max_length=255)),
                ("maker", models.BooleanField(db_column="maker")),
                ("order_id", models.CharField(db_column="orderId", max_length=255)),
                ("price", models.CharField(db_column="price", max_length=255)),
                ("qty", models.CharField(db_column="qty", max_length=255)),
                ("quote_qty", models.CharField(db_column="quoteQty", max_length=255)),
                (
                    "realized_pnl",
                    models.CharField(db_column="realizedPnl", max_length=255),
                ),
                ("side", models.CharField(db_column="side", max_length=255)),
                (
                    "position_side",
                    models.CharField(db_column="positionSide", max_length=255),
                ),
                ("symbol", models.CharField(db_column="symbol", max_length=255)),
                ("time", models.BigIntegerField(db_column="time")),
                (
                    "created_at",
                    models.DateTimeField(
                        db_column="createdAt", default=django.utils.timezone.now
                    ),
                ),
            ],
            options={
                "db_table": "Trades",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Transactions",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("symbol", models.CharField(db_column="symbol", max_length=255)),
                (
                    "income_type",
                    models.CharField(db_column="incomeType", max_length=255),
                ),
                ("income", models.CharField(db_column="income", max_length=255)),
                ("asset", models.CharField(db_column="asset", max_length=255)),
                ("info", models.CharField(db_column="info", max_length=255)),
                ("time", models.BigIntegerField(db_column="time")),
                ("tran_id", models.CharField(db_column="tranId", max_length=255)),
                ("trade_id", models.CharField(db_column="tradeId", max_length=255)),
                (
                    "created_at",
                    models.DateTimeField(
                        db_column="createdAt", default=django.utils.timezone.now
                    ),
                ),
            ],
            options={
                "db_table": "Transactions",
                "managed": False,
            },
        ),
    ]
