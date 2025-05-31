def generate_daily_advice(numerology_insights: dict, astrology_influences: dict) -> list:
    advice_items = []
    actions_to_do = []
    actions_to_avoid = []
    pd = numerology_insights.get("personal_day")

    # Numerology rules
    if pd == 1 or (isinstance(pd, str) and pd.startswith('1')):
        actions_to_do.append("Start new projects.")
    if pd == 4 or (isinstance(pd, str) and pd.startswith('4')):
        actions_to_do.append("Focus on practical tasks.")
    # ... extend with other numerology rules ...

    # Astrology rules
    if astrology_influences.get("mercury_retrograde"):
        actions_to_avoid.append("Sign major contracts without review; double-check communications.")
        actions_to_do.append("Review, reflect, reconnect (Re- activities).")

    transit_category = astrology_influences.get("key_transit_category")
    if transit_category == "Harmonious":
        actions_to_do.append("Leverage positive energies; things may flow easily.")
    if transit_category == "Challenging":
        actions_to_avoid.append("Force confrontations; push against strong resistance.")
        actions_to_do.append("Address necessary challenges with patience.")

    moon_sign = astrology_influences.get("transiting_moon_sign")
    if moon_sign in ["Aries", "Leo", "Sagittarius"]:
        actions_to_do.append("Act on inspiration; express yourself passionately.")
    elif moon_sign in ["Taurus", "Virgo", "Capricorn"]:
        actions_to_do.append("Focus on practical matters; ground yourself.")
    # ... add more rules as needed ...

    # Combined rules
    if (pd == 1 or (isinstance(pd, str) and pd.startswith('1'))) and transit_category == "Harmonious":
        advice_items.append("POWER DAY: Excellent energy for launching ventures with confidence!")

    # Consolidate advice
    if actions_to_do:
        advice_items.append("Consider DOING: " + "; ".join(set(actions_to_do)))
    if actions_to_avoid:
        advice_items.append("Consider AVOIDING: " + "; ".join(set(actions_to_avoid)))
    if not advice_items and not actions_to_do and not actions_to_avoid:
        advice_items.append("A general day. Follow your intuition.")

    return advice_items
