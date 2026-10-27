import React from 'react';
import clsx from 'clsx';
import {ThemeClassNames} from '@docusaurus/theme-common';
import useBaseUrl from '@docusaurus/useBaseUrl';
import SubscribeForm from '@site/src/components/SubscribeForm';

// Brand column (logo, one line on what Lumina is, newsletter signup) beside
// the link columns from docusaurus.config.js, then a slim bottom bar.
export default function FooterLayout({style, links, copyright}) {
  return (
    <footer
      className={clsx(ThemeClassNames.layout.footer.container, 'footer', 'lite-footer', {
        'footer--dark': style === 'dark',
      })}>
      <div className="container container-fluid">
        <div className="lite-footer__top">
          <div className="lite-footer__brand">
            <a href="https://www.lumina.ai/" target="_blank" rel="noopener noreferrer" aria-label="Lumina website">
              {/* The footer is always navy, so it uses the white primary logo. */}
              <img className="lite-footer__logo" src={useBaseUrl('/img/brand/lumina-logo-white.png')} alt="Lumina" width="147" height="28" />
            </a>
            <p className="lite-footer__tagline">One API for every model, in your code or behind your own gateway.</p>
            <p className="lite-footer__news-title">Get the latest Lumina updates</p>
            <p className="lite-footer__news-text">New model support, product launches, and release notes, in your inbox.</p>
            <SubscribeForm source="footer" tone="dark" />
          </div>
          <div className="lite-footer__links">{links}</div>
        </div>
        <div className="lite-footer__bottom">
          {copyright}
          <span className="lite-footer__legal">
            <a href="https://trust.lumina.ai/" target="_blank" rel="noopener noreferrer">
              SOC 2 Type II
            </a>
            <a href="https://github.com/Soventra/lumina/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">
              MIT license
            </a>
          </span>
        </div>
      </div>
    </footer>
  );
}
