import { Link } from 'react-router-dom';
import { Component } from 'react';

class BottomNav extends Component {

  render(){
    let { section, report } = this.props;
    let next = report.sections[section.number],
        previous = report.sections[section.number-2];

    return (
      <div className="report__bottom-nav">
        <div className="container">
        {previous &&
          <div className="report__bottom-nav__button previous">
            <Link to={`${report.url}${previous.slug}/`} className="button with-caret--left">Prev. Section</Link>
          </div>
        }
        {next &&
          <div className="report__bottom-nav__button next">
            <Link to={`${report.url}${next.slug}/`} className="button with-caret--right">Next Section</Link>
          </div>
        }
        </div>
      </div>
    );
  }
}

export default BottomNav;
