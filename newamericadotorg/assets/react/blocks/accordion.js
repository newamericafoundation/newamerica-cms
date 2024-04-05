import '../home-panels/pages/Jobs.scss';

import React, { Component } from 'react';
import { PlusX } from '../components/Icons';

const NAME = 'accordionBlock';
const ID = 'accordion-block';


class APP extends Component {
  state = {
    expanded: new Set()
  }

  toggleExpand = (i) => {
    let updated = new Set(this.state.expanded);
    if (updated.has(i)) {
      updated.delete(i);
    } else {
      updated.add(i);
    }
    this.setState({expanded: updated});
  }

  render() {
    let { items } = this.props;
    let { expanded } = this.state;
    let itemsArray = JSON.parse(items);
    return (
      <section className="padding-80">
        <div className="container--1080 home__fellowships">
          <div className="menu-list">
            {itemsArray.map((item, i) => (
              <div key={`accordion-${i}`} className={`${expanded.has(i) ? 'expanded ': ''}home__fellowship`}>
                <PlusX x={expanded.has(i)} />
                <h2 onClick={()=>{ this.toggleExpand(i) }}>{item.title}</h2>
                <div className="home__fellowship__more">
                  <div dangerouslySetInnerHTML={{__html: item.body }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    );
  }
}

export default { APP, NAME, ID, MULTI: true };
