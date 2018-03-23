import Subscribe, { List } from '../../program-page/components/Subscribe';
import { CheckBox, Text } from '../../components/Inputs';
import { Component } from 'react';
import Recaptcha from 'react-recaptcha';

class HomeSubscribe extends Subscribe {
  render(){
    let { programs, subscriptions } = this.props;
    let { params, posting, posted, status } = this.state;
    return (
      <div className={`margin-top-10`}>
        <div className={`home__subscribe ${this.state.shifted ? 'shifted' : ''}`}>
        <form onSubmit={this.submit} className="subscribe">
          <div>
            <div className="row gutter-10">
            <div className="subscribe__fields col-md-6">
              <Text name="email" label="Email" value={params.email} onChange={this.change} />
              <Text name="name" label="First Name & Last Name" value={params.name} onChange={this.change} />
              <Text name="organization" label="Organization" value={params.organization} onChange={this.change} />
              <Text name="job_title" label="Job Title" value={params.job_title} onChange={this.change} />
              <Text name="zipcode" label="Zipcode" value={params.zipcode} onChange={this.change} />
              {this.recaptcha()}
              <div className="desktop-submit">{this.submitButton()}</div>
            </div>
            <div className="subscribe__lists push-md-1 col-md-5">
              <div className="home__subscribe__toggles margin-top-25 margin-top-lg-0">
                <label className={`${this.state.shifted ? '' : 'bold'}`}
                  onClick={()=>{this.setState({ shifted: false})}}>
                  New America Lists
                </label>
                <span>|</span>
                <label className={`${this.state.shifted ? 'bold' : ''}`}
                  onClick={()=>{this.setState({ shifted: true})}}>
                  Program Lists
                </label>
              </div>
              <div className="primary margin-25">
                <List list={subscriptions} checked={this.state.subscriptions} toggle={this.toggleSubscription} />
              </div>
              <div className="secondary margin-25">
                <div>
                  {programs.map((p,i)=>{
                    if(!p.subscriptions) return null;
                    return (
                      <div key={`list-${i}`} className="subscribe__program-list">
                        <label className="block button--text margin-bottom-35">{p.title}</label>
                        <List list={p.subscriptions} checked={this.state.subscriptions} toggle={this.toggleSubscription} />
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
            <div className="mobile-submit">{this.submitButton()}</div>
            </div>
          </div>
        </form>
        </div>
      </div>
    );
  }
}

export default class SubscribeWrapper extends Component {

  render(){
    let { response : { results : { home_subscriptions, programs } } } = this.props;

    return (
      <HomeSubscribe subscriptions={home_subscriptions} programs={programs} />
    );
  }
}
