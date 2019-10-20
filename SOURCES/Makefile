PREFIX?=/usr
cfgdir?=/etc/molly-guard
libdir?=/lib
sbindir?=/sbin
REALPATH?=$(libdir)/molly-guard

all: molly-guard.8 shutdown

%.8: DB2MAN=/usr/share/sgml/docbook/xsl-stylesheets/manpages/docbook.xsl
%.8: XP=xsltproc -''-nonet
%.8: %.xml
	$(XP) $(DB2MAN) $<

man: molly-guard.8
	man -l $<
.PHONY: man

clean:
	rm -f shutdown
	rm -f molly-guard.8
.PHONY: clean

shutdown: shutdown.in
	sed -e 's,@cfgdir@,$(cfgdir),g;s,@REALPATH@,$(REALPATH),g' $< > $@

install: shutdown molly-guard.8
	mkdir -m755 --parent $(DESTDIR)$(libdir)/molly-guard
	install -m755 -oroot -oroot shutdown $(DESTDIR)$(libdir)/molly-guard/molly-guard
	
	mkdir -m755 --parent $(DESTDIR)$(cfgdir)
	install -m644 -oroot -oroot rc $(DESTDIR)$(cfgdir)
	cp -r run.d $(DESTDIR)$(cfgdir) \
	  && chown root.root $(DESTDIR)$(cfgdir)/run.d && chmod 755 $(DESTDIR)$(cfgdir)/run.d
	
	mkdir -m755 --parent $(DESTDIR)$(cfgdir)/messages.d
	
	mkdir -m755 --parent $(DESTDIR)$(PREFIX)/share/man/man8
	install -m644 -oroot -groot molly-guard.8 $(DESTDIR)$(PREFIX)/share/man/man8
.PHONY: install
