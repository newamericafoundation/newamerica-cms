import { Component, cloneElement } from 'react';
import { connect } from 'react-redux';
import { RadioButton } from './Inputs';
import { format as formatDate, subDays } from 'date-fns';
import { PlusX } from './Icons';

// must pass an response object from Fetch of Response component, history and location to FilterGroup
class _FilterGroup extends Component {
  componentDidMount(){
    this.reloadScrollEvents();
  }

  componentDidUpdate(prevProps){
    let { location, program, response } = this.props;

    if(location !== prevProps.location){
      this.reloadScrollEvents();
      if((window.scrollY > 300 || window.pageYOffset > 300) && document.documentElement.clientWidth > 992){
        window.scrollTo(0, 0);
      }
    }
  }

  reloadScrollEvents(){
    this.props.dispatch({
      type: 'RELOAD_SCROLL_EVENTS',
      component: 'site'
    });
  }

  render(){
      let { windowScrollPosition } = this.props;
      let remainder = document.body.offsetHeight - windowScrollPosition - 360 - 80;
      let maxHeight = remainder <= document.documentElement.clientHeight ? remainder : "calc(100vh)";
      if(document.documentElement.clientWidth < 992) maxHeight = 'none';
    return (
      <div className={`program__publications-filters scroll-target`} data-scroll-top-offset="-15"
      ref={(el)=>{this.el = el}}>
        <div className={`program__publications-filters__sticky-wrapper`}>
          <div className="program__publications-filters__scroll-wrapper">
          <div className="program__publications-filters__scroll-area"
            style={{
              maxHeight
            }}>
            {this.props.children.map( (c,i)=>( c ? cloneElement(c, {key: `filter-${i}`, ...this.props}) : null ) )}
          </div>
          </div>
        </div>
      </div>
    )
  }
}

const mapStateToProps = (state) => ({
 windowScrollPosition: state.site.scroll.position
});

export const FilterGroup = connect(mapStateToProps)(_FilterGroup);

export class Filter extends Component {
  constructor(props){
    super(props);
    this.state = {
      expanded: props.expanded || false
    }
  }

  handleChange = (event) => {}

  toggle = () => {
    this.setState({ expanded: !this.state.expanded });
  }

  label = () => {
    return (
      <h4 className="program__publications-filters__filter__heading margin-25" onClick={this.toggle}>
        {this.props.label}
        <div className="icon">
          <PlusX x={this.state.expanded} />
        </div>
      </h4>
    );
  }
}

export class TypeFilter extends Filter {
  handleChange = (event) => {
    let { history, location, programUrl } = this.props;
    let params = new URLSearchParams(location.search.replace('?', ''));
    if(event.target.value == 'otherpost'){
      params.delete('projectId');
      params.delete('topicId');
    } else {
      params.delete('category');
    }
    history.push(`${programUrl ? programUrl : '/'}${event.target.getAttribute('data-slug')}/?${params.toString()}`);
  }

  render(){
    let { types, location : { pathname }, response: { params: { query } } } = this.props;
    return (
      <div className={`program__publications-filters__filter type-filter ${this.state.expanded ? 'expanded' : ''}`}>
        {this.label()}
        <form>
          <RadioButton label={'All'} value={''} data-slug="publications" checked={query.content_type==undefined || pathname.indexOf('publications') != -1} onChange={this.handleChange} />
          {types.map((t,i)=>(
            <RadioButton key={`type-${i}`} label={t.title} value={t.api_name} data-slug={t.slug} checked={(query.content_type==t.api_name && (query.other_content_type_title==t.title || query.other_content_type_title==undefined))|| pathname.indexOf(`/${t.slug}/`) != -1} onChange={this.handleChange}/>
          ))}
        </form>
      </div>
    );
  }
}

export class CategoryFilter extends Filter {
  handleChange = (event) => {
    let { history, location, program } = this.props;
    let params = new URLSearchParams(location.search.replace('?', ''));

    if(event.target.value == '') {
      params.delete('category');
    } else {
      params.set('category', event.target.value);
    }

    history.push(`${location.pathname}?${params.toString()}`);
  }

  render(){
    let { categories, location : { pathname }, response: { params: { query } } } = this.props;
    return (
      <div className={`program__publications-filters__filter type-filter ${this.state.expanded ? 'expanded' : ''}`}>
        {this.label()}
        <form>
          <RadioButton label={'All'} value={''} checked={query.category==undefined} onChange={this.handleChange} />
          {categories.map((c,i)=>(
            <RadioButton key={`category-${i}`} label={c} value={c} checked={c==query.category} onChange={this.handleChange}/>
          ))}
        </form>
      </div>
    );
  }
}

export class ProgramFilter extends Filter {
  handleChange = (event) => {
    let { history, location } = this.props;
    let params = new URLSearchParams(location.search.replace('?', ''));
    if(event.target.value == '') {
      params.delete('programId');
    } else {
      params.set('programId', event.target.value);
    }

    history.push(`${location.pathname}?${params.toString()}`);
  }

  render(){
    let { programs, response: { params: { query } } } = this.props;

    return (
      <div className={`program__publications-filters__filter program-filter ${this.state.expanded ? 'expanded' : ''}`}>
        {this.label()}
        <form>
          <RadioButton label={'All'} value={''} checked={query.program_id==undefined} onChange={this.handleChange} />
          {programs.map((p,i)=>(
            <RadioButton key={`program-${i}`} label={p.title} value={p.id} checked={+query.program_id===p.id} onChange={this.handleChange}/>
          ))}
        </form>
      </div>
    );
  }
}

export class SubprogramFilter extends Filter {
  handleChange = (event) => {
    let { history, location, program } = this.props;
    let params = new URLSearchParams(location.search.replace('?', ''));

    if(event.target.value == '') {
      params.delete('projectId');
    } else {
      params.set('projectId', event.target.value);
    }

    history.push(`${location.pathname}?${params.toString()}`);
  }

  render(){
    let { subprograms, response: { params: { query } } } = this.props;
    return (
      <div className={`program__publications-filters__filter subprogram-filter ${this.state.expanded ? 'expanded' : ''}`}>
        {this.label()}
        <form>
          <RadioButton label={'All'} value={''} checked={query.subprogram_id==undefined} onChange={this.handleChange} />
          {subprograms.map((p,i)=>(
            <RadioButton key={`subprogram-${i}`} label={p.name} value={p.id} checked={+query.subprogram_id===p.id} onChange={this.handleChange}/>
          ))}
        </form>
      </div>
    );
  }
}

export class DateFilter extends Filter {
  constructor(props){
    super(props);
    this.state = {
      ...this.state,
      lastWeek: formatDate(subDays(new Date(), 7), 'YYYY-MM-DD'),
      lastMonth: formatDate(subDays(new Date(), 31), 'YYYY-MM-DD'),
      lastYear: formatDate(subDays(new Date(), 365), 'YYYY-MM-DD')
    }
  }
  handleChange = (event) => {
    let { history, location, program } = this.props;
    let params = new URLSearchParams(location.search.replace('?', ''));

    if(event.target.value == '') {
      params.delete('after');
    } else {
      params.set('after', event.target.value);
    }

    history.push(`${location.pathname}?${params.toString()}`);

  }

  render(){
    let { response: { params: { query } } } = this.props;
    let { lastWeek, lastMonth, lastYear } = this.state;
    return (
      <div className={`program__publications-filters__filter date-filter ${this.state.expanded ? 'expanded' : ''}`}>
        {this.label()}
        <form>
          <RadioButton label={'All'} value={''} checked={query.after==undefined} onChange={this.handleChange} />
          <RadioButton label={'In the Last Week'} value={lastWeek} checked={query.after==lastWeek} onChange={this.handleChange} />
          <RadioButton label={'In the Last Month'} value={lastMonth} checked={query.after==lastMonth} onChange={this.handleChange} />
          <RadioButton label={'In the Last Year'} value={lastYear} checked={query.after==lastYear} onChange={this.handleChange} />
        </form>
      </div>
    );
  }
}

export class TopicFilter extends Filter {
  constructor(props) {
    super(props);
    this.state = {
      ...this.state,
      topicArray: findTopicArray(+props.topicId, props.topics)
    }
  }

  componentWillReceiveProps(nextProps){
    if(nextProps.topicId != this.props.topicId)
      this.setState({ topicArray: findTopicArray(+nextProps.topicId, nextProps.topics)});
  }

  handleChange = (event) => {
    let { history, location, program } = this.props;
    let params = new URLSearchParams(location.search.replace('?', ''));

    if(event.target.value == '') {
      params.delete('topicId');
    } else {
      params.set('topicId', event.target.value);
    }

    history.push(`${location.pathname}?${params.toString()}`);
  }

  render(){
    let { topics, topicId } = this.props;
    let { topicArray } = this.state;

    let topicOptions = topicArray ? topicArray[topicArray.length-1].subtopics : topics;
    return (
      <div className={`program__publications-filters__filter topic-filter ${this.state.expanded ? 'expanded' : ''}`}>
        {this.label()}
        <form>
          {topicArray && <h5 className="clear-topics margin-top-0 margin-bottom-5" onClick={()=>{ this.handleChange({ target: { value: ''}}) }}>Reset</h5>}
          {topicArray && <ul className="topic-filter__selected-topics margin-bottom-25 margin-top-0">
            {topicArray.map((t,i)=>(
              <li key={`selected-topic-${i}`} onClick={()=>{ this.handleChange({ target: { value: t.id }}) }}>
                <h5 className="margin-0">{t.title}</h5>
              </li>
            ))}
          </ul>}
          <div className="topic-filter__topic-options">
            {topicOptions.map((t,i)=>(
              <RadioButton key={`topic-option-${i}`} label={t.title} value={t.id} checked={false} onChange={this.handleChange} />
            ))}
          </div>
        </form>
      </div>
    );
  }
}

function findTopic(id, topics){
  let queue = [...topics];
  let t;

  while(queue.length > 0){
    t = queue.shift();
    if(t.id == id) return t;
    for(let i = 0; i<t.subtopics.length; i++)
      queue.push(t.subtopics[i]);
  }

  return false;
}

function findTopicArray(id, topics, lineage=[]){

  for(let i = 0; i<topics.length; i++){
    if(topics[i].id==id) return [...lineage, topics[i]];
    let subtopic = findTopicArray(id, topics[i].subtopics, [...lineage, topics[i]]);
    if(subtopic) return subtopic;
  }

  return false;
}
