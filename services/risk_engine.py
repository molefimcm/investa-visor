# services/risk_engine.py
import os
import ctypes

_DLL_PATH = os.path.join(os.path.dirname(__file__), "..", "c_core", "risk_calc.dll")

def _risk_to_int(risk: str) -> int:
    risk = (risk or "").lower().strip()
    if risk == "conservative":
        return 0
    if risk == "aggressive":
        return 2
    return 1  # balanced default

def get_allocation(risk_appetite: str):
    """
    Returns dict like {"stocks": 60, "bonds": 35, "cash": 5}
    Falls back safely if DLL isn't available.
    """
    # Safe fallback (keeps MVP working even if C isn't built)
    fallback = {
        "conservative": {"stocks": 30, "bonds": 60, "cash": 10},
        "balanced": {"stocks": 60, "bonds": 35, "cash": 5},
        "aggressive": {"stocks": 80, "bonds": 15, "cash": 5},
    }
    risk_key = (risk_appetite or "balanced").lower().strip()
    if risk_key not in fallback:
        risk_key = "balanced"

    if not os.path.exists(_DLL_PATH):
        return fallback[risk_key]

    dll = ctypes.CDLL(_DLL_PATH)
    dll.allocation.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
    dll.allocation.restype = None

    stocks = ctypes.c_int()
    bonds = ctypes.c_int()
    cash = ctypes.c_int()

    dll.allocation(_risk_to_int(risk_appetite), ctypes.byref(stocks), ctypes.byref(bonds), ctypes.byref(cash))
    return {"stocks": stocks.value, "bonds": bonds.value, "cash": cash.value}
