import { Component } from 'react';
import { PlusX, Arrow } from '../components/Icons';
import { connect } from 'react-redux';

const NAME = 'scheduleBlock';
const ID = 'schedule-block';

class Session extends Component {
  render() {
    let { name, description, start_time, end_time, speakers, expanded, expand } = this.props;
    return (
      <div className={`schedule-block__sessions__session ${expanded ? 'expanded' : ''}`}>
        <PlusX onClick={expand} x={expanded} />
        <div className="schedule-block__sessions__session__heading margin-bottom-35">
          <div className="schedule-block__sessions__session__heading__title">
            <label className="block button--text">{start_time}{end_time && ' - '}{end_time}</label>
            <h3 className="margin-15">{name}</h3>
          </div>
          {description && <div className="post-body margin-35" dangerouslySetInnerHTML={{__html: description}} />}
        </div>
        {speakers &&
          <span>
            <label className="block button--text margin-bottom-35">Speakers</label>
            <div className="schedule-block__sessions__session__speakers">
              {speakers.map((s,i)=>(
                <div className="schedule-block__sessions__session__speakers__speaker margin-bottom-25">
                  <label className="bold block">{s.name}
                  {s.twitter &&
                    <a href={s.twitter} target="_blank">
                      <i className="fa fa-twitter"></i>
                    </a>}
                  </label>
                  {s.title && <label className="caption block">{s.title}</label>}
                </div>
              ))}
            </div>
          </span>
        }
      </div>
    );
  }
}


class APP extends Component {
  state = { }
  expand = (scheduleIndex) => {
    if(this.state[scheduleIndex]) this.setState({ [scheduleIndex]: false });
    else this.setState({ [scheduleIndex]: true });
  }
  render(){
    let { days } = this.props;
    if(!days) return null;
    days = JSON.parse(days);
    return (
      <div className={`schedule-block`}>
        {days.map((sessions,i)=>(
          <div className="schedule-block__day">
            <div className="schedule-block__sessions">
              {sessions.map((s,i)=>(
                <Session expanded={this.state[i]} expand={()=>{this.expand(i)}} {...s} />
              ))}
            </div>
          </div>
        ))}
      </div>
    );
  }
}



export default { APP, NAME, ID, MULTI: true };
