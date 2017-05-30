import { Fetch } from '../../components/API';
import { Component } from 'react';
import { connect } from 'react-redux';
import { NAME } from '../constants';
import Select from '../../components/Select';
import { Link } from 'react-router-dom';

class Filter extends Component {

  render(){
    let { programs, history, match } = this.props;
    let program = programs.find((p)=>p.slug==match.params.programSlug);
    return (
      <section className="container--medium people-filters">
        <Link to='/board'><label className="active">Board of Directors</label></Link>
        <Link to='/leadership'><label className="active">Leadership</label></Link>
        <Link to='/central-staff'><label className="active">Central Staff</label></Link>
        <Select
          name="Program"
          options={programs}
          defaultOption={program || {'slug': '', 'title': null}}
          className="people-filters__filter program"
          valueAccessor="slug"
          labelAccessor="title"
          onChange={(option)=>{
            if(!option) history.push('/our-people/');
            else history.push('/'+option.slug+'/our-people/');
          }}
          />
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
    page_size='12'
    page='1' />
)
