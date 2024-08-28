from functools import wraps
from django.http import HttpResponseRedirect
from django.urls import reverse
import logging
from .graph_api import get_user_groups_from_graph
from .views import obtener_access_token
logger = logging.getLogger(__name__)



def group_required(allowed_groups):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            token = obtener_access_token()  # Obtenemos el token usando la función simplificada
            correo = request.session.get('correo')
            
            if not token or not correo:
                logger.warning("Token de acceso o correo no encontrado.")
                # Redirigir al index con un mensaje de error
                request.session['error_message'] = "No tienes permiso para acceder a esta aplicación."
                return HttpResponseRedirect(reverse('index'))
            
            
            user_groups = get_user_groups_from_graph(token, correo)
            

            if not any(group in allowed_groups for group in user_groups):
                logger.warning(f"El usuario no pertenece a los grupos permitidos. Grupos del usuario: {user_groups}, Grupos permitidos: {allowed_groups}")
                # Redirigir al index con un mensaje de error
                request.session['error_message'] = "No tienes permiso para acceder a esta aplicación."
                return HttpResponseRedirect(reverse('index'))
            
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# decorators.py

"""logger = logging.getLogger(__name__)

def group_required(allowed_groups):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            token = obtener_access_token()  # Obtenemos el token usando la función simplificada
            correo = request.session.get('correo')
            
            if not token or not correo:
                logger.warning("Token de acceso o correo no encontrado.")
                return HttpResponseForbidden("No tienes permiso para acceder a esta aplicación.")
            
            logger.debug(f"Token de acceso obtenido: {token}")
            user_groups = get_user_groups_from_graph(token, correo)
            logger.debug(f"Grupos del usuario: {user_groups}")

            if not any(group in allowed_groups for group in user_groups):
                logger.warning(f"El usuario no pertenece a los grupos permitidos. Grupos del usuario: {user_groups}, Grupos permitidos: {allowed_groups}")
                return HttpResponseForbidden("No tienes permiso para acceder a esta aplicación.")
            
            logger.debug("Usuario permitido. Continuando con la vista.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator"""
