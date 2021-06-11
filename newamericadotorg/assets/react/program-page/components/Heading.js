import './Heading.scss';

import React, { Component } from 'react';
import { Link } from 'react-router-dom';

export default class Heading extends Component {

  render(){
    let { program } = this.props;

    return (
      <div className="program__header margin-bottom-10">
        <div className="program__heading__wrapper">
          {program.parent_programs &&
            <div className="program__header__back">
              {program.parent_programs.slice(0, 2).map((parent, i) => (
                <h6 className={`link with-caret--left margin-0 ${i > 0 && 'margin-top-5'}`}>
                  <a href={parent.url}>
                    <u>{parent.title}</u>
                  </a>
                </h6>
              ))}
            </div>}
          <h1 className="margin-0 promo">
            <Link to={program.url}>{program.title}</Link>
          </h1>
        </div>
      </div>
    );
  }
}
