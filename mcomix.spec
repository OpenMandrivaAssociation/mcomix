Summary:	MComix is a fork of the Comix project	
Name:		mcomix
Version:	0.95
Release:	2
License:	GPLv2+
Group:		Office
URL:		http://mcomix.sourceforge.net/
Source:		http://downloads.sourceforge.net/mcomix/%name-%{version}.tar.bz2

Buildarch:	noarch
BuildRequires:	python, python-imaging, jpeg-progs, pygtk2.0-devel
BuildRequires:	desktop-file-utils python-setuptools python-imaging-devel
Requires:	python, python-imaging, jpeg-progs, pygtk2.0 gettext
Patch0:		mcomix-0.92-fedora-rpmbuild-gtk.patch
Patch1:		mcomix-0.94-gettext-system-install.patch


%description
MComix is an user-friendly, customizable image viewer.
It is specifically designed to handle comic books, but also serves as
a generic viewer.  It reads images in ZIP, RAR, 7Zip or tar archives
as well as plain image files.  It is written in Python and uses GTK+
through the PyGTK bindings, and runs on both Linux and Windows.

%prep
%setup -q -n %{name}-%{version} 
%patch0 -p1
%patch1 -p1

%build
echo "Hey, i'm fake building "

find . -name comicthumb\* | while read f
do
	mv $f $(echo $f | sed -e 's|comicthumb|mcomicthumb|')
done
grep -rl comicthumb . | xargs sed -i -e 's|comicthumb|mcomicthumb|g'


%install
python setup.py \
	install \
	--root $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gconf/schemas
install -cpm 644 ./mime/comicbook.schemas \
	$RPM_BUILD_ROOT%{_sysconfdir}/gconf/schemas/%{name}.schemas


#localization
mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/
mv $RPM_BUILD_ROOT%{python_sitelib}/%{name}/messages/*/ \
	$RPM_BUILD_ROOT%{_datadir}/locale/


%find_lang %{name}

desktop-file-install --vendor='' \
	--dir %buildroot%_datadir/applications \
	--remove-category='Application' \
	--add-category='GNOME;GTK' \
	%buildroot%_datadir/applications/*.desktop

%post
%{update_desktop_database}
%{update_mime_database}

%postun
%{clean_desktop_database}
%{clean_mime_database}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING ChangeLog README

%{_sysconfdir}/gconf/schemas/%{name}.schemas
%{_bindir}/%{name}
%{python_sitelib}/%{name}/
%{python_sitelib}/%{name}-%{version}-py*.egg-info/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_mandir}/man1/mcomix.1*
%{_mandir}/man1/mcomicthumb.1*
%{_datadir}/icons/hicolor/*/apps/%{name}*
%{_datadir}/icons/hicolor/*/mimetypes/application-x-*.png
