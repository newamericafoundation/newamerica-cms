import { Component } from 'react';
import { Link } from 'react-router-dom';
import { Fetch } from '../../components/API';


class TypeFilter extends Component {
  constructor(props){
    super(props);
    this.state = {
      expanded: props.expanded || false
    }
  }

  handleChange = (event) => {
    let { setQueryParam, history, program } = this.props;
    setQueryParam('content_type', event.target.value);
    setQueryParam('page', 1, true);
    history.push(`${program.url}${event.target.getAttribute('data-slug')}/`);
  }

  toggle = () => {
    this.setState({ expanded: !this.state.expanded });
  }

  render(){
    let { types, setQueryParam, location : { pathname }, response: { params: { query } } } = this.props;
    return (
      <div className={`program__publications-filters__filter type ${this.state.expanded ? 'expanded' : ''}`}>
        <label className="program__publications-filters__filter__heading block bold margin-25" onClick={this.toggle}>
          Type
          <div className="icon">
            {this.state.expanded && <i className="fa fa-minus" />}
            {!this.state.expanded && <i className="fa fa-plus" />}
          </div>
        </label>
        <form>
          <label className="radio-button">All
            <input type="radio" value={''} data-slug={'publications'} checked={query.content_type=='' || pathname.indexOf('publications') != -1} onChange={this.handleChange}/>
            <div className="radio-button__indicator"></div>
          </label>
          {types.map((t,i)=>(
            <label className="radio-button">{t.name}
              <input type="radio" value={t.api_name} data-slug={t.slug} checked={query.content_type==t.api_name || pathname.indexOf(t.slug) != -1} onChange={this.handleChange}/>
              <div className="radio-button__indicator"></div>
            </label>
          ))}
        </form>
      </div>
    );
  }
}

export default class Filters extends Component {
  render(){
    let { program } = this.props;

    return (
      <div className="program__publications-filters">
        <TypeFilter types={program.content_types} {...this.props} expanded={true} />
      </div>
    )
  }
}
