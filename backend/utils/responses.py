from typing import Dict, Any, Optional

def success_response(
    data: Optional[Dict[str, Any]] = None,
    message: str = "Operación exitosa",
    status_code: int = 200
) -> Dict:
    """
    Genera una respuesta exitosa estandarizada
    
    Args:
        data: Datos a retornar
        message: Mensaje descriptivo
        status_code: Código HTTP de respuesta
        
    Returns:
        Diccionario con formato de respuesta estándar
    """
    response = {
        'success': True,
        'message': message,
        'status_code': status_code
    }
    if data:
        response['data'] = data
    return response

def error_response(
    message: str = "Error en la operación",
    status_code: int = 400,
    errors: Optional[Dict] = None
) -> Dict:
    """
    Genera una respuesta de error estandarizada
    
    Args:
        message: Mensaje de error
        status_code: Código HTTP de error
        errors: Detalles adicionales del error
        
    Returns:
        Diccionario con formato de error estándar
    """
    response = {
        'success': False,
        'message': message,
        'status_code': status_code
    }
    if errors:
        response['errors'] = errors
    return response
