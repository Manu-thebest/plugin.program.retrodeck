#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RetroDECK Launcher - addon de Kodi.

Al abrirlo: minimiza Kodi, lanza RetroDECK (Flatpak) y espera a que
termine; al salir de RetroDECK, restaura la ventana de Kodi.

Sin menús: es un lanzador directo, como un acceso directo del escritorio.
"""
import os
import subprocess
import sys

ADDON_PATH = os.path.dirname(os.path.abspath(__file__))
LIB_PATH = os.path.join(ADDON_PATH, 'resources', 'lib')
if LIB_PATH not in sys.path:
    sys.path.insert(0, LIB_PATH)

import xbmc
import xbmcgui
import xbmcplugin
import kodiutils as ku

HANDLE = int(sys.argv[1]) if len(sys.argv) > 1 else -1
DEFAULT_FLATPAK_ID = 'net.retrodeck.retrodeck'


def _build_command(app_id):
    """
    Construye el comando para lanzar RetroDECK.

    Si Kodi corre dentro de un sandbox Flatpak (variable FLATPAK_ID
    presente), un subprocess normal NO puede lanzar otro Flatpak: hay
    que usar 'flatpak-spawn --host' para salir del sandbox. Si Kodi
    corre nativo, llamamos a 'flatpak run' directamente.
    """
    if os.environ.get('FLATPAK_ID'):
        ku.log('Kodi en Flatpak (%s) -> flatpak-spawn --host'
               % os.environ.get('FLATPAK_ID'), xbmc.LOGINFO)
        return ['flatpak-spawn', '--host', 'flatpak', 'run', app_id]
    ku.log('Kodi nativo -> flatpak run directo', xbmc.LOGINFO)
    return ['flatpak', 'run', app_id]


def launch_retrodeck():
    app_id = ku.get_setting('retrodeck_flatpak_id') or DEFAULT_FLATPAK_ID
    minimize = ku.get_setting_bool('minimize_kodi')
    cmd = _build_command(app_id)

    xbmcgui.Dialog().notification('RetroDECK', 'Iniciando RetroDECK...',
                                  xbmcgui.NOTIFICATION_INFO, 2000)

    if minimize:
        ku.log('Minimizando Kodi', xbmc.LOGINFO)
        ku.try_minimize_kodi_window()

    ku.log('Lanzando: %s' % ' '.join(cmd), xbmc.LOGINFO)
    try:
        rc = subprocess.call(cmd)
    except Exception as e:
        ku.log('Error lanzando RetroDECK: %s' % e, xbmc.LOGERROR)
        rc = -1

    ku.log('RetroDECK terminó (rc=%s) -> restaurando Kodi' % rc, xbmc.LOGINFO)
    if minimize:
        ku.try_restore_kodi_window()

    if rc != 0:
        xbmcgui.Dialog().notification(
            'RetroDECK',
            'RetroDECK terminó con un aviso (código %s).' % rc,
            xbmcgui.NOTIFICATION_WARNING, 5000)


if __name__ == '__main__':
    launch_retrodeck()
    # No hay lista de elementos que mostrar: cerrar el directorio
    # para volver a la ventana desde la que se abrió el addon.
    if HANDLE >= 0:
        xbmcplugin.endOfDirectory(HANDLE, succeeded=False)
