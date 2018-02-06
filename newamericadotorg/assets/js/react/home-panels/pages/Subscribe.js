import Subscribe, { List } from '../../program-page/components/Subscribe';
import { CheckBox, Text } from '../../components/Inputs';
import { Component } from 'react';

class HomeSubscribe extends Subscribe {
  render(){
    let { programs, subscriptions } = this.props;
    let { params, posting, posted, status } = this.state;
    return (
      <div className={`container--1080 margin-top-10`}>
        <div className={`home__subscribe ${this.state.shifted ? 'shifted' : ''}`}>
        <form onSubmit={this.submit} className="subscribe">
          <div className="primary">
            <div className="row gutter-10">
            <div className="subscribe__fields col-md-6">
              <Text name="email" label="Email" value={params.email} onChange={this.change} />
              <Text name="name" label="First Name & Last Name" value={params.name} onChange={this.change} />
              <Text name="organization" label="Organization" value={params.organization} onChange={this.change} />
              <Text name="job_title" label="Job Title" value={params.job_title} onChange={this.change} />
              <Text name="zipcode" label="Zipcode" value={params.zipcode} onChange={this.change} />
              {this.submitButton()}
            </div>
            <div className="subscribe__lists push-md-1 col-md-5">
                <label className="block button--text margin-35">Lists</label>
                <List list={subscriptions} checked={this.state.subscriptions} toggle={this.toggleSubscription} />
            </div>
            <div className="home__subscribe__next">
              <a className={`button--text with-caret--${this.state.shifted ? 'left' : 'right'}`}
                onClick={()=>{this.setState({ shifted: !this.state.shifted})}}>
                {this.state.shifted ? 'Confirm' : 'View Program Lists' }
              </a>
            </div>
            </div>
          </div>
          <div className="secondary">
            <div className="secondary__wrapper">
              <div>
              {programs.map((p,i)=>{
                if(!p.subscriptions) return null;
                return (
                  <div className="subscribe__program-list">
                    <label className="block button--text margin-35">{p.title}</label>
                    <List list={p.subscriptions} checked={this.state.subscriptions} toggle={this.toggleSubscription} />
                  </div>
                );
              })}
            </div>
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
