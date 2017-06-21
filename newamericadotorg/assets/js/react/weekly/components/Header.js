const Header = ({ page }) => (
  <header className={`weekly-header ${page}`}>
    <div className="weekly-header__logo-wrapper">
      <a href="/"><div className="weekly-header__logo logo white sm"></div></a>
    </div>
    <div className="weekly-header__heading-wrapper">
      <a href="/weekly"><h1 className="weekly-header__heading">The Weekly</h1></a>
      <label className="active lg weekly-header__subheading">
        New Ideas and Voices in Policy. Delivered Every Thursday.
      </label>
    </div>
  </header>
);

export default Header;
