import { Component } from 'react';
import { connect } from 'react-redux';
import getNestedState from '../../../utils/get-nested-state';
import { setMenuState } from '../actions';

class Header extends Component {
  setMenuState = () => {
    let { menuIsOpen } = this.props;
    this.props.dispatch(setMenuState(!menuIsOpen));
  }
  render(){
    let { menuIsOpen, isArticle } = this.props;

    return(
      <header className='weekly-header'>
        <div className={`container weekly-header__container ${menuIsOpen ? 'with-open-menu' : ''}`}>
          <div className="row">
            <div className="col-3"><a href="/">
              <div className="weekly-header__logo logo sm white"></div></a>
            </div>
            <div className="weekly-header__title col-6">
              <div className="weekly-header__logo-wrapper">
                {/* <a href="/"><div className="weekly-header__logo logo white sm"></div></a> */}
              </div>
              <div className="weekly-header__title__wrapper">
                <a href="/weekly">
                  <h4 className="weekly-header__heading no-margin">The Weekly</h4>
                </a>
              </div>
            </div>
            <div className="col-3 weekly-header__more-editions">
              {!isArticle &&
                <button className={`weekly-header__more-editions__btn ${menuIsOpen ? 'active' : ''}`} onClick={this.setMenuState}>
                  More Editions
                </button>
              }
            </div>
          </div>
        </div>
      </header>
    );
  }
}

const mapStateToProps = (state) => ({
  menuIsOpen: getNestedState(state, 'weekly.edition.menuIsOpen')
})

export default connect(mapStateToProps)(Header);
