import React, { Component } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { CheckBox, Text } from '../../components/Inputs';
import { BASEURL } from '../../api/constants';
import { RECAPTCHA_SITE_KEY } from '../constants';
import Recaptcha from 'react-recaptcha';

const ConfirmationList = ({ subscriptionDefs, confirmedSubscriptions}) => (
    <ul>
      {subscriptionDefs.filter(d => confirmedSubscriptions.has(d.mailing_list_segment_id)).map((s,i)=>(
        <li key={`list-${i}`}><h6 className="margin-10">{s.title}</h6></li>
      ))}
    </ul>
  );

export class List extends Component {

  render(){
    let { list, checked, toggle } = this.props;
    return (
      <span>
      {list.map((s,i)=>(
        <div key={i} className="subscribe__field">
          <CheckBox checked={checked.has(s.mailing_list_segment_id)}
            name={s.title}
            value={s.title}
            label={s.title}
            onChange={()=>{toggle(s.title); }}/>
          <p>{s.search_description}</p>
        </div>
        ))}
      </span>
    );
  }
}

export function RecaptchaNotice() {
  return (
    <p className="recaptcha-notice">
      This site is protected by reCAPTCHA and the Google <a href="https://policies.google.com/privacy">Privacy Policy</a> and <a href="https://policies.google.com/terms">Terms of Service</a> apply.
    </p>
  );
}

export default class Subscribe extends Component {

  constructor(props){
    super(props);
    let params = new URLSearchParams(location.search.replace('?', ''))
    let subscriptions = new Set();

    if (props.subscriptions) {
      if (props.subscriptions.length === 1) {
        subscriptions.add(props.subscriptions[0].mailing_list_segment_id);
      } else {
        subscriptions = props.subscriptions.reduce(
          (result, {mailing_list_segment_id, checked_by_default}) => checked_by_default ? result.add(mailing_list_segment_id) && result: result,
          new Set()
        );
      }
    }
    let email = params.get('email') == 'null' ? '' : params.get('email');
    this.state = {
      csrf: '',
      posting: false,
      posted: false,
      status: 'OK',
      params: {
        email: email || '',
        name: '',
        zipcode: '',
      },
      subscriptions
    }

    let csrfCookieMatch = document.cookie.match(/csrftoken=(.*?)(;|$)/)
    if(csrfCookieMatch) this.state.csrf = csrfCookieMatch[1];
  }

  componentDidMount(){
    if(window.scrollY > 300 || window.pageYOffset > 300) window.scrollTo(0, 70);
    window.onloadCallback = this.onloadCallback;
    const script = document.createElement("script");

    script.src = "https://www.google.com/recaptcha/api.js?onload=onloadCallback&render=explicit";
    script.async = true;
    script.defer = true;

    document.body.appendChild(script);
    if(this.reloadScrollEvents) this.reloadScrollEvents()
  }

  lookupSegmentIdForTitle = (title) => {
    return this.props.subscriptions.find(
      subscription => subscription.title === title
    )?.mailing_list_segment_id
  }

  submit = (captchaResponse) => {
    if(this.state.posting || this.state.posted) return false;
    if(this.state.subscriptions.length === 0){
      this.setState({ status: 'NO_LIST' });
      return false;
    }

    let url = new URL(`${BASEURL}subscribe/`);

    for(let k in this.state.params)
      url.searchParams.append(k, this.state.params[k]);

    this.state.subscriptions.forEach(mailingListSegmentId => {
      url.searchParams.append('subscriptions[]', mailingListSegmentId);
    });

    url.searchParams.append("g-recaptcha-response", captchaResponse);

    this.setState({ posting: true });
    fetch(url, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': this.state.csrf
        }
      }).then(response => {
        return response.json();
      }).then( response => {

        this.setState({ posting: false, posted: true, status: response.status });
      });
  }

  verify = (response) => {
    this.submit(response);
  }

  onloadCallback = (response) => {
    //
  }

  change = (e, field) => {
    this.setState({
      params: {
        ...this.state.params,
        [e.target.getAttribute('name')]: e.target.value
      }
    });
  }

  toggleSubscription = (title) => {
    const mailingListSegmentId = this.lookupSegmentIdForTitle(title);
    if (mailingListSegmentId == null) {
      return;
    }
    this.setState(({subscriptions}) => {
      const newSubscriptions = new Set(subscriptions);
      if (subscriptions.has(mailingListSegmentId)) {
        newSubscriptions.delete(mailingListSegmentId);
      } else {
        newSubscriptions.add(mailingListSegmentId);
      }
      return {
        subscriptions: newSubscriptions
      }
    });
  }

  responseMessage = () => {
    let { status, posting, posted } = this.state;
    return (
      <>
        {posting && (
          <h6 className="button inline turquoise">
            <span className="loading-dots--absolute">
              <span>.</span><span>.</span><span>.</span>
            </span>
          </h6>)}
        {(posted && status=='OK') && <span>
                                       <h3>Thank you!</h3>
                                       <h6>You'll now start receiving emails from:</h6>
                                       <ConfirmationList
                                         subscriptionDefs={this.props.subscriptions}
                                         confirmedSubscriptions={this.state.subscriptions}/>
                                     </span>
        }
        {(status=='NO_LIST') && <h6 style={{ color: 'red' }} className="margin-15">Please check at least one subscription list</h6>}
        {status=='UNVERIFIED' && <h6>We're sorry. We were unable to verify that you're not a robot.</h6>}
        {(status!='OK' && status!='UNVERIFIED' && status!='NO_LIST') && <h6>We're sorry. Something went wrong. We've logged the error and will have a fix shortly.</h6>}
      </>
    );
  }

  render(){
    let { subscriptions } = this.props;
    let { params, posting, posted, status } = this.state;
    if(!subscriptions) return (
      <div className={`program__about program__subscribe margin-top-10`}>
      <h1>We're sorry!<br/>We don't have any subscription lists for you, yet.</h1>
      </div>
    );

    let recaptchaInstance;

    return (
      <div className={`program__about program__subscribe margin-top-10`}>
        <div className="container--1080">
          <form className="subscribe">
            <div className="row primary gutter-10">
              <div className={`subscribe__fields ${subscriptions.length > 1 && 'col-md-6'}`}>
                <Text name="email" label="Email" value={params.email} onChange={this.change} />
                <Text name="name" label="First Name & Last Name" value={params.name} onChange={this.change} />
                <Text name="zipcode" label="Zipcode" value={params.zipcode} onChange={this.change} required={false} />
              <Recaptcha
                ref={e => recaptchaInstance = e}
                sitekey={RECAPTCHA_SITE_KEY}
                render="explicit"
                onloadCallback={this.onloadCallback}
                verifyCallback={this.verify}
                size="invisible"
              />
              <div className="subscribe__submit margin-top-15">
                {!(posting || posted) && <input type="button" className="button" onClick={() => recaptchaInstance.execute()} value="Sign Up" />}
                {this.responseMessage()}
              </div>

                <RecaptchaNotice />
            </div>
            {subscriptions.length > 1 &&
             <div className="subscribe__lists push-md-1 col-md-5">
               <h5 className="margin-35">Lists</h5>
               <List list={subscriptions} checked={this.state.subscriptions} toggle={this.toggleSubscription} />
             </div>}
          </div>
        </form>
        </div>
      </div>
    );
  }
}
