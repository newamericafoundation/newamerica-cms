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
              <h6 className="program__header__back link margin-0 with-caret--left">
                <a href={program.parent_programs[0].url}>
                  <u>{program.parent_programs[0].title}</u>
                </a>
              </h6>}
              <h1 className="margin-0 promo">
                <Link to={program.url}>{program.display_logo_as_name && program.logo ? (
                  <img
                    className="program__heading__logo"
                    src={program.logo.url}
                    alt={program.logo.alt}
                  />
                ) : ( program.title )}
                </Link>
               </h1>
  			</div>
  		</div>
    );
  }
}
