import { Link } from 'react-router-dom';
import { Component } from 'react';

class BottomNav extends Component {

  render(){
    let { section, report } = this.props;
    let next = report.sections[section.number],
        previous = report.sections[section.number-2];

    return (
      <div className="report__bottom-nav">
        {previous &&
          <div className="report__bottom-nav__button previous">
            <Link to={`${report.url}${previous.slug}`}>
              <label className="white">Prev. Section</label>
            </Link>
          </div>
        }
        {next &&
          <div className="report__bottom-nav__button next">
            <Link to={`${report.url}${next.slug}`}>
              <label className="white">Next Section</label>
            </Link>
          </div>
        }
      </div>
    );
  }
}

export default BottomNav;
