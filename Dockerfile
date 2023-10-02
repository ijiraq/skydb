from almalinux:latest
# system settings and permissions needed for canfar/skaha science portal
RUN yum install -y sssd
COPY canfar/nofiles.conf /etc/security/limits.d/
COPY canfar/nsswitch.conf /etc/
## see https://bugzilla.redhat.com/show_bug.cgi?id=1773148
RUN touch /etc/sudo.conf && echo "Set disable_coredump false" > /etc/sudo.conf
COPY canfar/startup.sh /skaha/startup.sh
COPY etc/skydb.sh /etc/profile.d/skydb.sh
