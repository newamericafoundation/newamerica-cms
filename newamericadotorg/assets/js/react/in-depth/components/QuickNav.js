const getSectionUrl = (url) => {
  let relativeLink = /(\/in-depth\/.+)/.exec(url);
  if(relativeLink) return relativeLink[1];
  return false;
}

const QuickNav = ({ buttons, sections }) => (
  <nav className="in-depth__project__quick-nav">
    {buttons.length > 0 && <label className="lg active">Get Started:</label>}
    {buttons.map((b,i)=>(
      <div className="in-depth__project__quick-nav__item">
        {(i===0 && getSectionUrl(b.url)) &&
          <Link to={getSectionUrl(b.url)} className="button">
            {sections[0].title.indexOf(':')!=-1 ? sections[0].title : `Section 1: ${sections[0].title}` }
          </Link>
        }
        {(i>0 && getSectionUrl(b.url)) &&
          <Link to={getSectionUrl(b.url)} className="button white">{b.text}</Link>}
        {!getSectionUrl(b.url) &&
          <a href={b.url} className="button white">{b.text}</a>}
      </div>
    ))}
  </nav>
);

export default QuickNav;
