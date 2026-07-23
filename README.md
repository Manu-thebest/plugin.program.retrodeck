# RetroDECK Launcher (plugin.program.retrodeck)

Lanzador simple de **RetroDECK** (Flatpak) para Kodi. Sin menús: al abrir el addon se lanza RetroDECK directamente, como un acceso directo del escritorio.

## Qué hace

1. **Minimiza la ventana de Kodi** (vía libwnck del host, `XIconifyWindow` ICCCM — lo único que funciona con Marco/MATE; `wmctrl -b add,hidden` es ignorado por ese gestor de ventanas).
2. **Lanza RetroDECK**: `flatpak run net.retrodeck.retrodeck`.
3. **Espera** a que RetroDECK termine.
4. **Restaura y activa** la ventana de Kodi.

Funciona tanto con **Kodi nativo** como con **Kodi Flatpak** (usa `flatpak-spawn --host` automáticamente cuando detecta el sandbox).

## Requisitos

- RetroDECK instalado como Flatpak (`net.retrodeck.retrodeck`).
- Si Kodi es Flatpak: override `org.freedesktop.Flatpak=talk` (el mismo que usa el addon de Moonlight).
- En el host: `python3-gi` + `libwnck-3` (presente en cualquier escritorio MATE; lo usa mate-panel).

## Ajustes

| Ajuste | Defecto | Descripción |
|---|---|---|
| ID del Flatpak de RetroDECK | `net.retrodeck.retrodeck` | Por si cambia el ID de la app |
| Minimizar Kodi | `true` | Minimiza/restaura Kodi al lanzar/salir |
| Registro de depuración | `false` | Logs extra en kodi.log |

## Instalación

Descarga el ZIP desde [Releases](../../releases) e instálalo en Kodi con *Add-ons → Instalar desde un archivo zip*. Aparece en la sección **Programas**.
