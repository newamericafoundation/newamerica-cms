import './EndnoteAside.scss';

import React, { Component } from 'react';
import { PlusX } from '../../components/Icons';

class Endnote extends Component {
  cleanEndnote = () => {
    let { endnote : { note } } = this.props;

    let r = /((?:https?\:\/\/|www\.)[-A-Z0-9+&@#\/%?=~_|!:,.'’]*[-A-Z0-9+&@#\/%=~_|])/ig;
    return note.replace(r, function(url) {
        return '<a target="_blank" href="' + url + '">source</a>';
    });
  }
  render(){
    let { endnote, top, close } = this.props;

    return (
      <div className="report__body__endnote" style={{ top: top }}>
        <div className="report__body__endnote__close" onClick={close}>
          <PlusX x={true} />
        </div>
        {endnote &&<div className="report__body__endnote__text">
          <span>
            <h6 className="inline" >{`${endnote.number} `}</h6>
            <h6 className="inline" dangerouslySetInnerHTML={{__html: this.cleanEndnote()}}></h6>
          </span>
        </div>}
      </div>
    );
  }
}

export default Endnote;
