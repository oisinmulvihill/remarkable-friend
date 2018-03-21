# -*- coding: utf-8 -*-
"""
"""


def document_id_and_extension(filename):
    """Recover the document id and extension from the raw notebook filename.

    :param filename: E.g. 12d97066-9881-44b6-9abc-2284855f43a1.lines

    :returns: ('12d97066-9881-44b6-9abc-2284855f43a1', 'lines')

    """
    file_name_parts = filename.split('.')

    extension = ''
    document_id = file_name_parts[0].strip()
    if len(file_name_parts) > 1:
        extension = file_name_parts[-1].strip()

    return (document_id, extension)
