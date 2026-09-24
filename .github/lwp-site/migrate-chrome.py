#!/usr/bin/env python3
"""One-time, idempotent migration of the vendored guide and comparison chrome."""
from pathlib import Path
import re,json
root=Path(__file__).resolve().parent/'sources'
for m in root.rglob('manifest.json'):
 if '/templates/kits/' not in m.as_posix():continue
 kit=m.parent;d=json.loads(m.read_text());name=d.get('id')
 if name not in ('lightwebpres-docs','field-notes'):continue
 css=kit/'structure.css';text=css.read_text()
 if 'Kit containers own spacing;' in text or 'Ruled masthead is kit structure;' in text:continue
 if name=='lightwebpres-docs':
  text=re.sub(r'\.lwp-presentation--lightwebpres-docs \.lwp-doc-frame \.slide-chrome-(header|footer)[^{]*\{[^}]*\}', '', text)
  text+='''\n/* Kit containers own spacing; native chrome visuals come from the theme. */
.lwp-presentation--lightwebpres-docs .doc-masthead{position:relative;z-index:2;margin-bottom:clamp(28px,5vh,54px)}
.lwp-presentation--lightwebpres-docs .doc-colophon{position:relative;z-index:1;margin-top:clamp(28px,5vh,52px)}
.lwp-presentation--lightwebpres-docs .doc-masthead:empty,.lwp-presentation--lightwebpres-docs .doc-colophon:empty{display:none}
'''
  header,footer='doc-masthead','doc-colophon'
  props={'slide-header.gap':'10px','slide-header.logo-size':'28px','slide-footer.padding-block':'14px','slide-footer.rule-fg':'#0B254533','slide-footer.rule-width':'1px'}
 else:
  text=re.sub(r'\.lwp-presentation--field-notes \.slide-chrome-(header|footer|icon)[^{]*\{[^}]*\}', '', text)
  text+='''\n/* Ruled masthead is kit structure; native text and asset sizing stay typed. */
.lwp-presentation--field-notes .field-masthead{padding-bottom:12px;border-bottom:2px solid var(--color-ink)}
.lwp-presentation--field-notes .field-masthead:empty,.lwp-presentation--field-notes .field-colophon:empty{display:none}
'''
  header,footer='field-masthead','field-colophon'
  props={'slide-header.font':"'Nimbus Mono PS', 'Courier New', 'Liberation Mono', 'DejaVu Sans Mono', monospace",'slide-header.size':'max(12px, 1.5vmin)','slide-header.weight':'bold','slide-header.tracking':'0.12em','slide-header.gap':'12px','slide-header.logo-size':'32px','slide-footer.font':"'Nimbus Mono PS', 'Courier New', 'Liberation Mono', 'DejaVu Sans Mono', monospace",'slide-footer.size':'max(12px, 1.5vmin)','slide-footer.tracking':'0.08em','slide-footer.padding-block':'12px','slide-footer.rule-fg':'#111111FF','slide-footer.rule-width':'1px'}
 css.write_text(text)
 for h in (kit/'slides').rglob('*.html'):
  t=h.read_text().replace('{{slide_header}}',f'<div class="{header}">{{{{slide_header}}}}</div>').replace('{{slide_footer}}',f'<div class="{footer}">{{{{slide_footer}}}}</div>')
  h.write_text(t)
 for theme in (kit/'themes').glob('*.conf'):
  text=theme.read_text();text+='\n# Native chrome uses the typed Theme registry.\n'
  for key,v in props.items():text+=key+': '+v+'\n'
  theme.write_text(text)
for lang in ['en','fr']:
 (root/'comparisons'/lang/'nebula/templates/settings.conf').write_text('# Use the selected appearance from series.json; no local property pins.\n')

(root.parent/'migration-state.json').write_text(json.dumps({'schema':1,'native_chrome':'typed-theme','canonical_sources':'sources','legacy_transfers':'retired'},indent=2)+'\n')
