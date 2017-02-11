from ludema import exceptions
from ludema.abstract.piece import Piece

def copy_lists_in_dictionary(dict):
    """
    Args:
        dict (dict): just any dictionary.

    Returns:
        New dictionary with a shallow copy of the lists present on
        the original dictionary.
    """
    new_dict = {}
    for k, v in dict.items():
        if isinstance(v, list):
            v = v.copy()
        new_dict[k] = v
    return new_dict

def extract_pieces_from_possible_containers(container):
    """Grabs a container, which from we can hopefully extract a list.

    Args:
        container (nullary function -> Piece | [Piece] | Piece): the container for the Piece

    Returns:
        Piece: the piece which was in the container

    Raises:
        ImpossibleToExtractPiece, if the container is not of correct type.

    Note:
        If type(container) == list, this function pops the last element and
        modifies the list.

    """
    if callable(container):  # most probably a nullary function
        piece = container()
    elif isinstance(container, list):
        piece = container.pop()
    else: # we just have to hope this is a piece, really
        piece = container

    # if your final product was a not a piece, we've got a problem
    if not isinstance(piece, Piece):
        raise exceptions.ImpossibleToExtractPiece(container)
    return piece
