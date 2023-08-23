def get_main_role(top, jungle, mid, bot, sup):
    role_list = [top, jungle, mid, bot, sup]
    role = max(role_list)

    if role == top:
        return "TOP"
    elif role == jungle:
        return "JUNGLE"
    elif role == mid:
        return "MIDDLE"
    elif role == bot:
        return "BOTTOM"
    elif role == sup:
        return "SUPPORT"