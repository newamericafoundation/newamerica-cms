import React, { Component } from 'react';
import { Link } from 'react-router-dom';

export class Promo extends Component {
  render(){
    let { title, linkTo } = this.props;

    return (
      <div className="card promo row gutter-0">

          <div className="promo__heading col-12 col-lg-2">
            {linkTo && <Link to={linkTo}>
              <h5 className="white margin-0">{title}</h5>
            </Link>}
            {!linkTo &&
              <h5 className="white margin-0">{title}</h5>
            }
          </div>

          <div className="card__text col-12 col-lg-10">
            {linkTo && <Link to={linkTo}>
              {this.props.children}
            </Link>}
            {!linkTo && this.props.children}
          </div>

      </div>
    );
  }
}

export class PromoMd extends Component {
  render(){
    let { title, link : { label, to }} = this.props;

    return (
      <div className="card promo-md">
        <div className="card__text">
          <h6 className="margin-top-0">{title}</h6>
          {this.props.children}
        </div>
        <div className="card__link-to">
          <Link to={to} className="button--text link with-caret--right">
            {label}
          </Link>
        </div>
      </div>
    );
  }
}
