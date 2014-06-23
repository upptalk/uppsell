from django.db import IntegrityError

#====================================================================================
# Workflow transitions
#====================================================================================

class CancelTransition(Exception):
    """Cancel the current transition"""
    pass
class BadTransition(CancelTransition):
    """The current transition is not allowed"""
    pass

#====================================================================================
# Coupon errors
#====================================================================================

class CouponSpendError(Exception):
    """Coupon could not be used"""
    pass

class CouponLimitError(CouponSpendError):
    """Coupon could not be used: limit execeded"""
    pass
class CouponDoubleSpendError(Exception):
    """Coupon could not be used: user has already spent it"""
    pass
class CouponDateError(Exception):
    """Coupon could not be used: out of date"""
    pass

#====================================================================================
# Model errors
#====================================================================================

class StateError(IntegrityError):
    """The model does not allow that operation due to current workflow state"""
    pass
    

