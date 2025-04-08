from datetime import datetime


"""
    PARSEA o Convierte una fecha (string como '22 jan 2025') a un objeto datetime.
    Que es el formato ISO 8601.
    
    :param date_str: Fecha en formato de cadena (string).
    :return: Objeto datetime
"""

def parse_datetime_to_iso_format(date_str: str) -> datetime:

    if isinstance(date_str, str):
        try:
            # Intentar convertir al formato 'YYYY-MM-DDTHH:MM:SS'
            print("____________1er TRY-EXCEPT fecha de tipo STRING_____________", date_str)
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            # Si no coincide con el formato 'YYYY-MM-DDTHH:MM:SS', intentar con el formato 'DD MMM YYYY'
            # Se realiza esta validación por el body que envía el Frontend (22 Jan 2025)
            try:
                print("____________2DO TRY EXCEPT fecha de tipo STRING_____________", date_str)
                return datetime.strptime(date_str, "%d %b %Y")
            except ValueError:
                    # Si el formato no es válido, lanzar un error
                raise ValueError('Invalid date format, expected format is either "YYYY-MM-DDTHH:MM:SS" or "DD MMM YYYY"')
        
    # Si ya es un datetime, devolverlo tal cual
    elif isinstance(date_str, datetime):
        print("_____ELIF___einvoice_dto.py____es un datetime", date_str)
        return date_str
    else:
        raise ValueError(f"Invalid date format: {type(date_str)}")


