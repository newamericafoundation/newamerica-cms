import { Component } from 'react';

class Social extends Component {
  social = () => {
    let icons = [
      {
        label: 'Share', icon: 'fa-facebook', id: 'social__facebook',
        url: `https://www.facebook.com/dialog/share?app_id=1650004735115559&display=popup&href=${location.origin + this.props.url}`
      },
      { label: 'Tweet', icon: 'fa-twitter', id: 'social__twitter',
        url: `https://twitter.com/intent/tweet/?url=${location.origin + this.props.url}&text=${`${this.props.title}`}&via=newamerica`
      }
    ];

    if(this.props.report_pdf){
      icons.push(
        { label: 'Download', icon: 'fa-download', id: 'social__download', url: `${this.props.url}pdf/`  }
      );
    }
    return icons;
  }
  render(){
    return (
      <div className="report__social">
        {this.social().map((s, i)=>(
          <div className={`report__social__item margin-bottom-25 ${s.id}`} key={`social-${i}`}>
            <a href={s.url} target="_blank" >
              <i className={`fa circle ${s.icon}`} />
              <h6 className="margin-0 inline">{s.label}</h6>
            </a>
          </div>
        ))}
      </div>
    );
  }
}

export default Social;
