audio-hw-socket
===============

Some vendor audio HALs (Xiaomi devices with Elliptic ultrasound proximity,
e.g. tucana) take a listening socket from Android init via
`android_get_control_socket("audio_hw_socket")`. Clients such as the
Elliptic sensor HAL connect to `/dev/socket/audio_hw_socket` and send
`ultrasound-proximity=1/0`. On stock Android only `vendor.audio-hal-2-0`
gets that socket.

On Sailfish OS the HAL is loaded inside the user PulseAudio
(pulseaudio-modules-droid*), so this package:

- lets group `audio` create sockets in `/dev/socket` (sticky, mode 1775),
- binds `/dev/socket/audio_hw_socket` from the user systemd instance and
  passes it to `pulseaudio.service`,
- exports `ANDROID_SOCKET_audio_hw_socket=<fd>` before exec'ing PulseAudio,
- keeps the path hidden (`/dev/socket/.audio_hw_socket`) while PulseAudio
  is not ready, because the HAL crashes if it accepts a request while
  module-droid-card is still loading.

Disable without uninstalling (as the session user):

    systemctl --user mask audio-hw-socket.socket
    systemctl --user restart pulseaudio
