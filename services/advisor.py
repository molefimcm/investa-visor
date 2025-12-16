def classify_investor(profile):
    risk = profile["risk_appetite"]
    horizon = profile["time_horizon"]

    if risk == "conservative":
        return "Capital Preserver"
    if risk == "aggressive" and horizon == "long":
        return "Growth Accumulator"
    if risk == "balanced":
        return "Balanced Long-Term Builder"
    return "Steady Investor"


def allocation(profile):
    risk = profile["risk_appetite"]

    if risk == "conservative":
        return {"Equities": 30, "Bonds": 50, "Cash": 20}
    if risk == "aggressive":
        return {"Equities": 80, "Bonds": 10, "Cash": 10}
    return {"Equities": 60, "Bonds": 25, "Cash": 15}


def principles(profile):
    exp = profile["experience_level"]

    base = [
        "Invest consistently on a fixed schedule",
        "Avoid reacting to short-term market noise",
        "Review your plan annually, not daily"
    ]

    if exp == "beginner":
        base.append("Prefer simple, diversified instruments")
    else:
        base.append("Focus on asset allocation over individual picks")

    return base
