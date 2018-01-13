import { Component } from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Fetch } from '../../components/API';
import ScrollArea from 'react-scrollbar';

class Filter extends Component {
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
      <label className="program__publications-filters__filter__heading block bold margin-25" onClick={this.toggle}>
        {this.props.label}
        <div className="icon">
          {this.state.expanded && <i className="fa fa-minus" />}
          {!this.state.expanded && <i className="fa fa-plus" />}
        </div>
      </label>
    );
  }
}

const RadioButton = (props) => (
  <label className="radio-button">{props.label}
    <input type="radio" {...props} />
    <div className="radio-button__indicator"></div>
  </label>
)

class TypeFilter extends Filter {
  handleChange = (event) => {
    let { setQuery, history, location, program } = this.props;
    let params = new URLSearchParams(location.search.replace('?', ''));
    setQuery({
      content_type: event.target.value,
      page: 1
    }, true);
    history.push(`${program.url}${event.target.getAttribute('data-slug')}/?${params.toString()}`);
  }

  render(){
    let { types, setQueryParam, location : { pathname }, response: { params: { query } } } = this.props;
    return (
      <div className={`program__publications-filters__filter type ${this.state.expanded ? 'expanded' : ''}`}>
        {this.label()}
        <form>
          <RadioButton label={'All'} value={''} data-slug="publications" checked={query.content_type=='' || pathname.indexOf('publications') != -1} onChange={this.handleChange} />
          {types.map((t,i)=>(
            <RadioButton label={t.name} value={t.api_name} data-slug={t.slug} checked={query.content_type==t.api_name || pathname.indexOf(t.slug) != -1} onChange={this.handleChange}/>
          ))}
        </form>
      </div>
    );
  }
}

class SubprogramFilter extends Filter {
  handleChange = (event) => {
    let { setQueryParam, history, location, program } = this.props;
    let params = new URLSearchParams(location.search.replace('?', ''));

    if(event.target.value == '') {
      params.delete('subprogramId');
    } else {
      params.set('subprogramId', event.target.value);
    }

    history.push(`${location.pathname}?${params.toString()}`);
    setQueryParam('subprogram_id', event.target.value, true);

  }

  render(){
    let { subprograms, response: { params: { query } } } = this.props;
    return (
      <div className={`program__publications-filters__filter type ${this.state.expanded ? 'expanded' : ''}`}>
        {this.label()}
        <form>
          <RadioButton label={'All'} value={''} checked={query.subprogram_id==''} onChange={this.handleChange} />
          {subprograms.map((p,i)=>(
            <RadioButton label={p.name} value={p.id} checked={+query.subprogram_id===p.id} onChange={this.handleChange}/>
          ))}
        </form>
      </div>
    );
  }
}

class DateFilter extends Filter {
  handleChange = (event) => {}

  render(){
    return (
      <div className={`program__publications-filters__filter type ${this.state.expanded ? 'expanded' : ''}`}>
        {this.label()}
        <form>
        </form>
      </div>
    );
  }
}

class TopicFilter extends Filter {
  handleChange = (event) => {}

  render(){
    return (
      <div className={`program__publications-filters__filter type ${this.state.expanded ? 'expanded' : ''}`}>
        {this.label()}
        <form>
        </form>
      </div>
    );
  }
}

class Filters extends Component {
  state = { lastScrollPosition: 0 }

  componentDidMount(){
    this.reloadScrollEvents();
  }

  componentDidUpdate(prevProps){
    let { location, program, setQuery } = this.props;
    if(location !== prevProps.location){
      this.reloadScrollEvents();
      let slug = location.pathname.match(/.+\/(.+)\/$/i)[1];
      let type = program.content_types.find((t)=>(t.slug === slug));
      // if(+document.body.style.top.replace('px', '') < -365){
      //   this.state.lastScrollPosition = 365;
      //   this.enableScroll();
      //   this.disableScroll(false);
      // }
      if(window.scrollY > 300){
        window.scrollTo(0, 300);
      }
    }
  }

  disableScroll = (update) => {
    // if(update !== false) this.state.lastScrollPosition = this.props.windowScrollPosition;
    // document.body.classList.add('scroll-disabled');
    // document.body.style.top = -this.state.lastScrollPosition + 'px';
  }

  enableScroll = () => {
    // document.body.classList.remove('scroll-disabled');
    // document.body.style.top = '';
    // window.scrollTo(0, this.state.lastScrollPosition);
  }

  reloadScrollEvents(){
    this.props.dispatch({
      type: 'RELOAD_SCROLL_EVENTS',
      component: 'site'
    });
  }

  render(){
    let { program, response } = this.props;

    return (
      <div className={`program__publications-filters scroll-target`}
        data-scroll-top-offset="-15"
        onMouseEnter={this.disableScroll}
        onTouchStart={this.disableScroll}
        onMouseLeave={this.enableScroll}
        onTouchEnd={this.enableScroll}>
        <div className={`program__publications-filters__sticky-wrapper ${response.isFetching ? 'is-fetching' : ''}`}>
          <ScrollArea className="program__publications-filters__scroll-area">
            <TypeFilter types={program.content_types} {...this.props} expanded={true} label="Type"/>
            <SubprogramFilter subprograms={program.subprograms} {...this.props} label="Subprogram"/>
            <DateFilter {...this.props} label="Date"/>
            <TopicFilter {...this.props} label="Topic"/>
          </ScrollArea>
        </div>
      </div>
    )
  }
}

const mapStateToProps = (state) => ({
  windowScrollPosition: state.site.scroll.position
});

export default connect(mapStateToProps)(Filters);
