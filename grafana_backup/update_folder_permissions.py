import json
from grafana_backup.dashboardApi import update_folder_permissions, get_team_by_name


def main(args, settings, file_path):
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers = settings.get('HTTP_POST_HEADERS')
    http_get_headers = settings.get('HTTP_GET_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    with open(file_path, 'r') as f:
        data = f.read()

    folder_permissions = json.loads(data)
    if folder_permissions:
        # PROBLEM:
        # 1. grafana_backup can't create team with same id as in backup (api limitations)
        # 2. grafana uses only team id to update folder permissions
        # That's means impossibility to use api export + import without workarounds
        # WORKAROUND:
        # Find the real team id by name before updating folder permissions
        for fp in folder_permissions:
            if fp['teamId'] > 0:
                result = get_team_by_name(fp['team'], grafana_url,
                                          http_get_headers, verify_ssl, client_cert, debug)
                if result > 0:
                    fp['teamId'] = result

        result = update_folder_permissions(folder_permissions, grafana_url, http_post_headers, verify_ssl, client_cert, debug)
        print("update folder permissions {0}, status: {1}, msg: {2}\n".format(folder_permissions[0].get('title', ''), result[0], result[1]))
