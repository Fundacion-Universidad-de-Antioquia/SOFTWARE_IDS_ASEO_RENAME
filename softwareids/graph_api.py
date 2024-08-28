import requests
import logging

logger = logging.getLogger(__name__)
import requests
import requests
import logging

logger = logging.getLogger(__name__)

"""def get_user_groups_from_graph(token):
    logger.debug(f"Obteniendo grupos con el token: {token}")
    
    graph_url = "https://graph.microsoft.com/v1.0/me/memberOf"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    
    response = requests.get(graph_url, headers=headers)
    
    if response.status_code == 200:
        groups = response.json().get('value', [])
        group_names = [group['displayName'] for group in groups]
        logger.debug(f"Grupos obtenidos: {group_names}")
        return group_names
    else:
        logger.error(f"Error al obtener grupos: {response.status_code} - {response.text}")
        return []
"""

# graph_api.py

def get_user_groups_from_graph(token, user_principal_name):
    
    graph_url = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}/memberOf"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    
    response = requests.get(graph_url, headers=headers)
    
    if response.status_code == 200:
        groups = response.json().get('value', [])
        group_names = [group['displayName'] for group in groups if group['@odata.type'] == '#microsoft.graph.group']
        
        return group_names
    else:
        logger.error(f"Error al obtener grupos: {response.status_code} - {response.text}")
        return []
