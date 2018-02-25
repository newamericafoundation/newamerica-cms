import { Component } from 'react';

class Social extends Component {
  social = () => {
    let icons = [
      { label: 'Share', icon: 'fa-facebook', id: 'social__facebook', url: '' },
      { label: 'Tweet', icon: 'fa-twitter', id: 'social__twitter', url: '' }
    ];
    
    if(this.props.report_pdf){
      icons.push(
        { label: 'Download', icon: 'fa-download', id: 'social__download', url: `${this.props.report_pdf}`  }
      );
    }
    return icons;
  }
  render(){
    return (
      <div className="report__social">
        {this.social().map((s, i)=>(
          <div className={`report__social__item margin-bottom-15 ${s.id}`} key={`social-${i}`}>
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
