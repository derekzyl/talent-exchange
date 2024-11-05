def getList(select: str) -> tuple[list | None, list | None]:
    if select is None:
        return [], []
    get_list = [field.strip() for field in select.split(",")]
    add_field = [field[1:] for field in get_list if not field.startswith("-")]
    remove_field = [field[1:] for field in get_list if field.startswith("-")]
    return add_field, remove_field
