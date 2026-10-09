Name:       audio-hw-socket
Summary:    Pass Android's audio_hw_socket to the audio HAL inside PulseAudio
Version:    1.0.0
Release:    1
License:    BSD-3-Clause
Source0:    %{name}-%{version}.tar.bz2
BuildArch:  noarch
Requires:   pulseaudio
Requires:   systemd

%description
Some vendor audio HALs (e.g. Xiaomi devices with Elliptic ultrasound
proximity) listen on /dev/socket/audio_hw_socket, which Android init
creates only for vendor.audio-hal-2-0. On Sailfish OS the HAL is loaded
inside the user PulseAudio instead, so the user systemd instance binds the
socket and passes it to PulseAudio as ANDROID_SOCKET_audio_hw_socket.

%prep
%setup -q -n %{name}-%{version}

%build

%install
install -D -m 0644 tmpfiles/audio-hw-socket.conf %{buildroot}/usr/lib/tmpfiles.d/audio-hw-socket.conf
install -D -m 0644 systemd/audio-hw-socket.socket %{buildroot}/usr/lib/systemd/user/audio-hw-socket.socket
install -D -m 0644 systemd/50-audio-hw-socket.conf %{buildroot}/usr/lib/systemd/user/pulseaudio.service.d/50-audio-hw-socket.conf
install -D -m 0755 pulseaudio-audio-hw-socket %{buildroot}/usr/libexec/pulseaudio-audio-hw-socket
mkdir -p %{buildroot}/usr/lib/systemd/user/sockets.target.wants
ln -s ../audio-hw-socket.socket %{buildroot}/usr/lib/systemd/user/sockets.target.wants/audio-hw-socket.socket

%post
systemd-tmpfiles --create /usr/lib/tmpfiles.d/audio-hw-socket.conf || :

%files
%defattr(-,root,root,-)
/usr/lib/tmpfiles.d/audio-hw-socket.conf
/usr/lib/systemd/user/audio-hw-socket.socket
/usr/lib/systemd/user/sockets.target.wants/audio-hw-socket.socket
/usr/lib/systemd/user/pulseaudio.service.d/50-audio-hw-socket.conf
/usr/libexec/pulseaudio-audio-hw-socket
