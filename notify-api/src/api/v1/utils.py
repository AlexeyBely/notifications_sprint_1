def collect_user_variables(user_id: str, info_users: dict) -> dict:
    """Collect user variables into a single dictionary."""

    return info_users[user_id]


def collect_film_variables(info_films: list) -> dict:
    """Collect films variables into a single dictionary."""

    film_var = {}
    num_film = 1
    for info_film in info_films:
        for key in info_film:
            var_name = f'film_{num_film}_{key}'
            film_var[var_name] = info_film[key]
        num_film += 1
    return film_var
