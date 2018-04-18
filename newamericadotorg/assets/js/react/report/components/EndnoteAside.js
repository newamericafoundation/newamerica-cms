import { Component } from 'react';
import { PlusX } from '../../components/Icons';

class Endnote extends Component {
  cleanEndnote = () => {
    let { endnote : { note } } = this.props;
    let r = /(http.+?)(;| |$|<)/g
    let matches = note.match(r);
    if(matches){
      for(let m of matches){
        m = m.replace(';', '').replace('<', '');
        note = note.replace(m, `<a href="${m}" target="_blank">source</a>`);
      }
    }

    return note;
  }
  render(){
    let { endnote, top } = this.props;

    return (
      <div className="report__body__endnote" style={{ top: top }}>
        <div className="report__body__endnote__close" onClick={this.props.close}>
          <PlusX x={true} />
        </div>
        {endnote &&<span>
          <label className="inline" >{`${endnote.number} `}</label>
          <label className="inline" dangerouslySetInnerHTML={{__html: this.cleanEndnote()}}></label>
        </span>}
      </div>
    );
  }
}

export default Endnote;
