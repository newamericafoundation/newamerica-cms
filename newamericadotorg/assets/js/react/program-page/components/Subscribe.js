import { Component } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { CheckBox, Text } from '../../components/Inputs';
import { BASEURL } from '../../api/constants';

export class List extends Component {

  render(){
    let { list, checked, toggle } = this.props;
    return (
      <span>
      {list.map((s,i)=>(
        <div className="subscribe__field">
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
    let subscriptions = null;
    if(props.subscriptions){
      subscriptions = props.subscriptions.map((s,i)=>(s.title))
    }
    this.state = {
      csrf: '',
      posting: false,
      posted: false,
      status: 'OK',
      params: {
        email: params.get('email'),
        name: null,
        organization: null,
        job_title: null,
        zipcode: null
      },
      subscriptions
    }

    let csrfCookieMatch = document.cookie.match(/csrftoken=(.*?)(;|$)/)
    if(csrfCookieMatch) this.state.csrf = csrfCookieMatch[1];
  }

  componentDidMount(){
    if(window.scrollY > 300) window.scrollTo(0, 70);
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
          'X-CSRFToken': this.csrf
        }
      }).then(response => {
        return response.json();
      }).then( response => {

        this.setState({ posting: false, posted: true, status: response.status });
      });
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
            </div>
            <div className="subscribe__lists push-md-1 col-md-5">
                <label className="block button--text margin-35">Lists</label>
                <List list={subscriptions} checked={this.state.subscriptions} toggle={this.toggleSubscription} />
                <div className="subscribe__submit">
                  {(!posting && !posted) && <input type="submit" className="button turquoise" value="Sign Up" />}
                  {posting && <label className="button turquoise"><span className="loading-dots--absolute">
                    <span>.</span><span>.</span><span>.</span>
                  </span></label>}
                  {(posted && status=='OK') && <h3>Thank you!</h3>}
                  {status!='OK' && <label className='block'>We're sorry. Something went wrong. We've logged the error and will have a fix shortly.</label>}
                </div>
            </div>
          </div>
        </form>
        </div>
      </div>
    );
  }
}
