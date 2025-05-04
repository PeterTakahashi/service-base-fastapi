def get_file_extension(filename: str | None) -> str:
    """
    Get the file extension from the filename.
    """
    if not filename:
        return ""
    return filename.split(".")[-1] if "." in filename else ""
