import { Component } from 'react';

class Social extends Component {
  social = () => {
    return [
      { label: 'Share', icon: 'fa-facebook', id: 'social__facebook', url: '' },
      { label: 'Tweet', icon: 'fa-twitter', id: 'social__twitter', url: '' },
      { label: 'Download', icon: 'fa-download', id: 'social__download', url: `${this.props.url}pdf/`  },
      { label: 'Print', icon: 'fa-print', id: 'social__print', url: '' }
    ];
  }
  render(){
    return (
      <div className="report__social">
        {this.social().map((s)=>(
          <div className={`report__social__item ${s.id}`}>
            <a href={s.url} target="_blank" >
              <i className={`fa ${s.icon}`} />
              <label>{s.label}</label>
            </a>
          </div>
        ))}
      </div>
    );
  }
}

export default Social;
