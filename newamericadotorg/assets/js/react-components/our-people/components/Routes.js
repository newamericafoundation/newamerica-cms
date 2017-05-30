import { Route, Switch } from 'react-router-dom';
import Filter from './PeopleFilter';
import { connect } from 'react-redux';

let Heading = ({title, programs, programSlug }) => (
  <div className="people-list__heading">
    <h1>{(programSlug ? programs.find((p)=>p.slug==programSlug).title : '')+title}</h1>
  </div>
);

const mapStateToProps = state => ({
  programs: state.programData.results || []
});

Heading = connect(mapStateToProps)(Heading);

export const Routes = () => (
  <Switch>
    <Route path="/board" render={(props)=>(
      <section>
        <Heading title='Board'/>
        <Filter {...props} />
      </section>
    )}/>
    <Route path="/leadership" render={(props)=>(
      <section>
        <Heading title='Leadership'/>
        <Filter {...props} />
      </section>
    )}/>
    <Route path="/our-people" render={(props)=>(
      <section>
        <Heading title='Our People'/>
        <Filter {...props} />
      </section>
    )}/>
    <Route path="/central-staff" render={(props)=>(
      <section>
        <Heading title='Central Staff'/>
        <Filter {...props} />
      </section>
    )}/>
    <Route path="/:programSlug/our-people/" render={(props)=>(
      <section>
        <Heading programSlug={props.match.params.programSlug} title=' People'/>
        <Filter {...props} />
      </section>
    )}/>
  </Switch>
)
