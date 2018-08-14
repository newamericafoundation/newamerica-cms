import React, { Component } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { CheckBox, Text } from '../../components/Inputs';
import { BASEURL } from '../../api/constants';
import Recaptcha from 'react-recaptcha';

const ConfirmationList = ({ subscriptions }) => (
    <ul>
      {subscriptions.map((s,i)=>(
        <li key={`list-${i}`}><h6 className="margin-10">{s}</h6></li>
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
          <CheckBox checked={checked.indexOf(s.title)>=0}
            name="subscriptions[]"
            value={s.title}
            label={s.alternate_title || s.title}
            onChange={()=>{toggle(s.title); }}/>
          <p>{s.search_description}</p>
        </div>
        ))}
      </span>
    );
  }
}

export default class Subscribe extends Component {

  constructor(props){
    super(props);
    let params = new URLSearchParams(location.search.replace('?', ''))
    let subscriptions = [];
    // if(props.subscriptions){
    //   subscriptions = props.subscriptions.map((s,i)=>(s.title))
    // }
    let email = params.get('email') == 'null' ? '' : params.get('email');
    this.state = {
      csrf: '',
      posting: false,
      posted: false,
      status: 'OK',
      params: {
        email: email || '',
        name: '',
        organization: '',
        job_title: '',
        zipcode: '',
        'g-recaptcha-response': undefined
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

  submit = (e) => {
    e.preventDefault();
    if(this.state.posting || this.state.posted) return false;

    let url = new URL(`${BASEURL}subscribe/`);

    for(let k in this.state.params)
      url.searchParams.append(k, this.state.params[k]);

    for(let i=0; i<this.state.subscriptions.length; i++)
      url.searchParams.append('subscriptions[]', this.state.subscriptions[i]);


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
    this.setState({ params: {
      ...this.state.params,
      'g-recaptcha-response': response
    }});
  }

  onloadCallback = (response) => {
    //
  }

  recaptcha = () => {
    return (
      <Recaptcha
        sitekey="6LeZg04UAAAAAGmXngof3LCn4FJUYTfDnxv7qmSg"
        render="explicit"
        onloadCallback={this.onloadCallback}
        verifyCallback={this.verify}
      />
    )
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
    let subscriptions;
    let i = this.state.subscriptions.indexOf(title);
    if(i==-1) {
      subscriptions = [...this.state.subscriptions, title];
    } else {
      subscriptions = [...this.state.subscriptions]
      subscriptions.splice(i,1);
    }
    this.setState({ subscriptions });
  }

  submitButton = () => {
    let { posting, posted, status } = this.state;
    if(!this.state.params['g-recaptcha-response']) return null;
    return (
      <div className="subscribe__submit margin-top-15">
        {(!posting && !posted) && <input type="submit" className="button" value="Sign Up" />}
        {posting &&
          <h6 className="button inline turquoise">
            <span className="loading-dots--absolute">
              <span>.</span><span>.</span><span>.</span>
            </span>
          </h6>}
        {(posted && status=='OK') && <span>
            <h3>Thank you!</h3>
            <h6>You'll now start receiving emails from:</h6>
            <ConfirmationList subscriptions={this.state.subscriptions}/>
          </span>
        }
        {status=='UNVERIFIED' && <h6>We're sorry. We were unable to verify that you're not a robot.</h6>}
        {(status!='OK' && status!='UNVERIFIED') && <h6>We're sorry. Something went wrong. We've logged the error and will have a fix shortly.</h6>}
      </div>
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

    return (
      <div className={`program__about program__subscribe margin-top-10`}>
        <div className="container--1080">
        <h1>Subscribe</h1>
        <form onSubmit={this.submit} className="subscribe">
          <div className="row primary gutter-10">
            <div className="subscribe__fields col-md-6">
              <Text name="email" label="Email" value={params.email} onChange={this.change} />
              <Text name="name" label="First Name & Last Name" value={params.name} onChange={this.change} />
              <Text name="organization" label="Organization" value={params.organization} onChange={this.change} />
              <Text name="job_title" label="Job Title" value={params.job_title} onChange={this.change} />
              <Text name="zipcode" label="Zipcode" value={params.zipcode} onChange={this.change} />
              {this.recaptcha()}
              {this.submitButton()}
            </div>
            <div className="subscribe__lists push-md-1 col-md-5">
                <h5 className="margin-35">Lists</h5>
                <List list={subscriptions} checked={this.state.subscriptions} toggle={this.toggleSubscription} />
            </div>
          </div>
        </form>
        </div>
      </div>
    );
  }
}
