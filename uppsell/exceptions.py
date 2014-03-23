
class CouponLimitError(Exception):
    """Coupon could not be used: limit execeded"""
    pass
class CouponSpendError(Exception):
    """Coupon could not be used: user has already spent it"""
    pass

