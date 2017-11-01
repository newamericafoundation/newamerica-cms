import { Component } from 'react';

class Endnote extends Component {

  render(){
    let { endnote, top } = this.props;

    return (
      <div className="report__body__endnote" style={{ top: top }}>
        <div className="report__body__endnote__close" onClick={this.props.close}>x</div>
        {endnote &&<span>
          <label className="inline" >{`${endnote.number} `}</label>
          <label className="inline" dangerouslySetInnerHTML={{__html: endnote.note}}></label>
        </span>}
      </div>
    );
  }
}

export default Endnote;
