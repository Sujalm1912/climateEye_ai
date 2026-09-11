"""
Chat Service for ClimateEYE AI Assistant
Processes queries with awareness of active location and real-time weather context.
"""

def generate_chat_response(message, context):
    """
    Generate an intelligent, context-aware climate assistant response.
    message: User query string
    context: Dict containing location and real-time weather data
    """
    if not message or not message.strip():
        return "Please ask a question about the active climate zone or atmospheric conditions."

    msg = message.strip().lower()
    loc = context.get("location") or "the selected location"
    weather = context.get("weather") or {}

    temp = weather.get("temperature")
    feels = weather.get("apparent_temperature")
    humidity = weather.get("relative_humidity")
    cloud = weather.get("cloud_cover")
    precip = weather.get("precipitation", 0.0)
    wind = weather.get("wind_speed")
    condition = weather.get("condition") or "Moderate"
    units = weather.get("units", {})
    t_unit = units.get("temperature", "°C")
    w_unit = units.get("wind_speed", "km/h")

    # 1. Climate Summary / Overview
    if any(k in msg for k in ["summary", "overview", "report", "what's the weather", "current weather", "how is it"]):
        return (
            f"📊 **Climate Summary for {loc}**:\n\n"
            f"• **Condition**: {condition} with {cloud}% cloud cover.\n"
            f"• **Temperature**: {temp}{t_unit} (Feels like {feels}{t_unit}).\n"
            f"• **Atmospheric Moisture**: {humidity}% relative humidity.\n"
            f"• **Precipitation**: {precip} mm recorded.\n"
            f"• **Wind Speed**: {wind} {w_unit}.\n\n"
            f"Overall, current conditions are **{condition.lower()}** with a thermal index of {feels}{t_unit}."
        )

    # 2. Rain / Precipitation
    if any(k in msg for k in ["rain", "precipitat", "umbrella", "shower", "storm"]):
        if precip and float(precip) > 0.0:
            return f"🌧️ Yes, active precipitation is recorded in **{loc}** with **{precip} mm** currently. Carrying an umbrella or rain protection is recommended!"
        elif "rain" in condition.lower() or "drizzle" in condition.lower():
            return f"🌦️ Current atmospheric reports indicate **{condition}** in **{loc}**, though measurable ground accumulation is minimal ({precip} mm)."
        else:
            return f"☀️ There is currently **no active precipitation** in **{loc}** ({precip} mm recorded). Sky is {condition.lower()} with {cloud}% cloud cover."

    # 3. Temperature / Feels Like
    if any(k in msg for k in ["temp", "heat", "warm", "cold", "feels like", "hot"]):
        comfort = "hot and muggy" if feels and feels > 35 else "warm" if feels and feels > 28 else "comfortable" if feels and feels > 20 else "cool"
        diff = ""
        if feels and temp and feels > temp:
            diff = f" (humidity makes it feel {round(feels - temp, 1)}{t_unit} warmer)"
        elif feels and temp and feels < temp:
            diff = f" (wind makes it feel {round(temp - feels, 1)}{t_unit} cooler)"
        return f"🌡️ The ambient temperature in **{loc}** is **{temp}{t_unit}**, and it feels like **{feels}{t_unit}**{diff}. Conditions feel **{comfort}**."

    # 4. Humidity / Moisture
    if any(k in msg for k in ["humid", "moisture", "dew"]):
        h_rating = "very humid" if humidity and humidity > 70 else "moderately humid" if humidity and humidity > 45 else "dry"
        return f"💧 Relative humidity in **{loc}** is **{humidity}%**, which is considered **{h_rating}**."

    # 5. Wind
    if any(k in msg for k in ["wind", "breeze", "gust"]):
        w_rating = "strong breeze" if wind and wind > 25 else "moderate breeze" if wind and wind > 12 else "light breeze / calm"
        return f"💨 The wind speed in **{loc}** is measured at **{wind} {w_unit}** ({w_rating}) at 10m height."

    # 6. Outdoor Activities / Exercise
    if any(k in msg for k in ["outdoor", "run", "walk", "exercise", "safe", "go out"]):
        advice = []
        if feels and feels > 38:
            advice.append("Stay hydrated and avoid strenuous direct-sun exposure due to elevated apparent heat.")
        if precip and float(precip) > 0.5:
            advice.append("Wear rain gear or plan indoor activities.")
        if not advice:
            advice.append("Conditions are suitable for typical outdoor movement.")
        return f"🏃 **Outdoor Advisory for {loc}**:\n" + "\n".join(f"• {a}" for a in advice)

    # Generic contextual fallback
    return (
        f"I'm synchronized with live telemetry for **{loc}**.\n\n"
        f"Current state: **{temp}{t_unit}** ({condition}), **{humidity}%** humidity, "
        f"and **{wind} {w_unit}** wind. Feel free to ask about precipitation risk, thermal comfort, or an atmospheric summary!"
    )
