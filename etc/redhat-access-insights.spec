%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define _binaries_in_noarch_packages_terminate_build 0

Name:                   redhat-access-insights
Summary:                Uploads Insights information to Red Hat on a periodic basis
Version:                1.0.7
Release:                3%{?dist}
Source0:                https://github.com/redhataccess/insights-client/archive/redhat-access-insights-%{version}.tar.gz
Epoch:                  0
License:                GPLv2+
URL:                    http://access.redhat.com/insights
Group:                  Applications/System
Vendor:                 Red Hat, Inc.

Obsoletes: redhat-access-proactive

Requires: python
Requires: python-setuptools
Requires: python-requests >= 2.6
Requires: python-magic
Requires: libcgroup
Requires: tar
Requires: gpg
Requires: pciutils
%if 0%{?rhel} && 0%{?rhel} > 6
Requires: libcgroup-tools
%endif
BuildArch: noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools

%description
Sends insightful information to Red Hat for automated analysis

%prep
%setup -q

%install
rm -rf ${RPM_BUILD_ROOT}
%{__python} setup.py install --root=${RPM_BUILD_ROOT} $PREFIX

%post
#Migrate existing machine-id
if  [ -f "/etc/redhat_access_proactive/machine-id" ]; then
mkdir -p /etc/redhat-access-insights/
mv /etc/redhat_access_proactive/machine-id /etc/redhat-access-insights/machine-id
fi

%postun
if [ "$1" -eq 0 ]; then
rm -f /etc/cron.daily/redhat-access-insights
rm -f /etc/cron.weekly/redhat-access-insights
rm -f /etc/redhat-access-insights/.cache*
rm -f /etc/redhat-access-insights/.registered
rm -f /etc/redhat-access-insights/.unregistered
fi

%clean
test "x$RPM_BUILD_ROOT" != "x" && rm -rf $RPM_BUILD_ROOT

%files
%defattr(755,root,root)
%{_bindir}/redhat-access-insights
/etc/redhat-access-insights/redhat-access-insights.cron

%defattr(0600, root, root)
%dir /etc/redhat-access-insights
%config(noreplace) /etc/redhat-access-insights/*.conf
/etc/redhat-access-insights/.fallback.json
/etc/redhat-access-insights/.fallback.json.asc
/etc/redhat-access-insights/redhattools.pub.gpg
/etc/redhat-access-insights/.exp.sed
/etc/redhat-access-insights/*.pem

%defattr(-,root,root)
%{python_sitelib}/redhat_access_insights*.egg-info
%{python_sitelib}/redhat_access_insights/*.py*

%doc
/usr/share/man/man8/*.8.gz
/usr/share/man/man5/*.5.gz

%changelog
* Wed Jan 06 2016 Jeremy Crafts <jcrafts@redhat.com> - 1.0.7-3
- New config options trace and no_schedule
- New command line options --no_schedule, --conf, --to-stdout, --compressor, --from-stdin, --support, --offline, and --status
- Add certificate chain verification to connection test
- Revised debug output
- Reduced set of environment vars used for command execution
- OpenStack cluster support
- Remember time of last successful upload
- Resolves: bz1237112, bz1243028, bz1244113, bz1246919, bz1250384, bz1257242, bz1267299, bz1276055, bz1276130, bz1280353, bz1295929, bz1295935, bz1295939 

* Mon Jun 08 2015 Dan Varga <dvarga@redhat.com> - 1.0.4-0
- Improved logging of exceptions
- Redact passwords automatically

* Mon Jun 01 2015 Dan Varga <dvarga@redhat.com> - 1.0.3-0
- New default URLs
- New config file format
- Default to auto configuration

* Mon May 18 2015 Dan Varga <dvarga@redhat.com> - 1.0.2-0
- Update man pages

* Thu May 07 2015 Dan Varga <dvarga@redhat.com> - 1.0.1-0
- Add man pages
- New certificate chain for cert-api.access.redhat.com
- Better auto configuration for satellite installations

* Wed Apr 29 2015 Dan Varga <dvarga@redhat.com> - 1.0.0-2
- Drop min python-requests version to 2.4

* Mon Apr 27 2015 Dan Varga <dvarga@redhat.com> - 1.0.0-1
- Add LICENSE file
- Resolves: bz1215002

* Thu Apr 23 2015 Dan Varga <dvarga@redhat.com> - 1.0.0-0
- Initial build
- Resolves: bz1176237
