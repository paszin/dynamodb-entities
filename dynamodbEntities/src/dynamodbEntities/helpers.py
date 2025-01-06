
def get_default_lookup(entities_import):
    """
    usage:
    import entities
    lookup = get_default_lookup(entities)
    """
    return {c: getattr(entities_import, c) for c in dir(entities_import) if not c.startswith("_")}
