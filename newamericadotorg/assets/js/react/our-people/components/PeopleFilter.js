import { Fetch } from '../../components/API';
import { Component } from 'react';
import { connect } from 'react-redux';
import { NAME } from '../constants';
import Select from '../../components/Select';
import { Link, Route } from 'react-router-dom';

let paths = [
  {path: '/our-people/', title: 'All Staff', role: ''},
  {path: '/board/', title: 'Board of Directors', role: 'Board Member'},
  {path: '/leadership/', title: 'Leadership', role: ''},
  {path: '/our-people/programs/', title: 'Program Staff', role: 'Program Staff'},
  {path: '/central-staff/', title: 'Central Staff', role: 'Central Staff'},
  {path: '/:programSlug/our-people/', title: '', role: ''}
];

const Links = ({selected}) => (
  <div className="inline-toggles">
    {paths.filter((p)=>(p.title!=='')).map((p)=>(
      <div className={"inline-toggles__item" + (selected==p.path ? ' selected' : '') }>
        <Link to={p.path}>{p.title}</Link>
      </div>
    ))}
  </div>
)

class Filter extends Component {
  defaultQuery = {
    program_slug: '',
    program_id: '',
    role: '',
    leadership: '',
    role: '',
    page: 1
  }

  componentWillUpdate(nextProps) {
    let { match, setQuery } = this.props;
    let query = this.defaultQuery;

    if(match.path != nextProps.match.path) {
      let role;
      switch(nextProps.match.path){
        case '/our-people/':
        case '/board/':
        case '/central-staff/':
          role = paths.find((p)=>p.path==nextProps.match.path).role;
          setQuery({ ...query, role }, true);
          break
        case '/our-people/programs/':
          role = 'Program Staff';
          let program_id = this.getProgramId(nextProps.location);
          setQuery({ ...query, program_id, role }, true);
          break;
        case '/:programSlug/our-people':
          let program_slug = match.params.programSlug || '';
          setQuery({ ...query, program_slug }, true);
          break;
        case '/leadership/':
          setQuery({ ...query, leadership: 'True' }, true);
          break;
        default:
          setQuery(query, true);
      }
    }
  }

  getProgramId = (location) => {
    let query = new URLSearchParams(location.search);
    return query.get('program_id') ? query.get('program_id') : '';
  }

  render(){
    let { programs, history, match, location, setQuery } = this.props;

    return (
      <section className="our-people__heading container--medium">
        <div className="our-people__filters inline-toggles-wrapper">
          {match.path!='/:programSlug/our-people/' &&
            <Links selected={match.path} />
          }
        </div>
          <Route path="/our-people/programs/" render={(props)=>(
            <div className="our-people__filters__select-wrapper">
              <Select
                name="Program"
                options={programs}
                className="people-filters__filter program wide"
                valueAccessor="id"
                labelAccessor="title"
                onChange={(option)=>{
                  let val = option ? '?program_id='+option.id : '';
                  props.history.push('/our-people/programs/'+val);
                  let page = 1;
                  let program_id = option ? option.id : '';
                  setQuery({ page, program_id }, true)
                }}/>
              </div>
          )}/>
      </section>
    );
  }
}

const mapStateToProps = state => ({
  programs: state.programData.results || []
});

Filter = connect(mapStateToProps)(Filter);

export default (props) => (
  <Fetch {...props}
    name={NAME}
    component={Filter}
    fetchOnMount={true}
    endpoint='author'
    initialQuery={{
      page_size: 24,
      page: 1,
      program_id: new URLSearchParams(location.search).get('program_id') ? new URLSearchParams(location.search).get('program_id') : '',
      program_slug: props.match.params.programSlug ? props.match.params.programSlug : '',
      leadership: props.match.path == '/leadership/' ? 'True' : '',
      role: paths.find((p)=>p.path==props.match.path).role
    }} />
)
