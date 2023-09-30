from django.contrib import admin

from .models import Code, MonthlyCheckinReward, RotationLuckReward


class CodeAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "coin_price", "user")
    # list_filter = ("is_read",)
    search_fields = ["name", "code", "user"]
    # prepopulated_fields = {"tag": ("number",)}


class RotationLuckRewardAdmin(admin.ModelAdmin):
    list_display = ("code_with_coin_price", "coin", "rate")
    # list_filter = ("is_read",)
    search_fields = ["code_with_coin_price", "coin"]
    # prepopulated_fields = {"tag": ("number",)}


class MonthlyCheckinRewardAdmin(admin.ModelAdmin):
    list_display = ("month", "year", "day_count", "coin")
    # list_filter = ("is_read",)
    search_fields = ["month", "year"]
    # prepopulated_fields = {"tag": ("number",)}


admin.site.register(Code, CodeAdmin)
admin.site.register(RotationLuckReward, RotationLuckRewardAdmin)
admin.site.register(MonthlyCheckinReward, MonthlyCheckinRewardAdmin)
