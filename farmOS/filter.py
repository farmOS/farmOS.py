def filter(path, value, operation="="):
    """Helper method to build JSONAPI filter query params."""

    # TODO: Validate path, value, operation?
    # TODO: Support filter groups.
    # TODO: Support revision filters, are these edge cases?
    # TODO: Support "pagination" query params? Separate method?
    # TODO: Support "sort" query params? Separate method?
    # TODO: Support "includes" query params? Separate method?

    filters = {}

    # If the operation is '=', only one query param is required.
    if operation == "=":
        param = f"filter[{path}]"
        filters[param] = value
    # Else we need a query param for the path, operation, and value.
    else:
        # TODO: Use a unique identifier instead of using "condition"
        # otherwise the same path cannot be filtered multiple times.
        base_param = f"filter[{path}_{operation.lower()}][condition]"

        path_param = base_param + "[path]"
        filters[path_param] = path

        op_param = base_param + "[operator]"
        filters[op_param] = operation

        value_param = base_param + "[value]"
        if operation in ["IN", "NOT IN", ">", "<", "<>", "BETWEEN"]:
            value_param += "[]"
        filters[value_param] = value

    return filters
