# -*- coding: utf-8 -*-
"""
"""
import pathlib


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


def filename_from(document_id, extension, path=None):
    """Convert to the filename with optional path.

    :param document_id: UUID string.

    :param extension: file ending e.g. lines, metadata.

    :param path: A optional path to prepend to the filename.

    :returns: <path>/<filename>

    """
    if extension == 'backup':
        filename = '{}.lines.{}'.format(document_id, extension)

    else:
        if extension:
            filename = '.'.join([document_id, extension])
        else:
            filename = document_id

    if path:
        filename = str(pathlib.Path(path) / filename)

    return filename
