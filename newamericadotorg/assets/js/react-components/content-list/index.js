import { NAME, ID } from './constants';
import SiteFilter from './components/SiteFilter';
import ContentList from './components/ContentList';
import { BrowserRouter, Route, Link, Switch } from 'react-router-dom';
import { Component } from 'react';
import { connect } from 'react-redux';

class App extends Component {
  render() {
    let { contentTypes } = this.props;

    return (
      <BrowserRouter>
        <section className="content-list-wrapper container">
          <Switch>
            <Route path='/publications' render={(props)=>(
              <SiteFilter {...props}
                contentType={{slug: 'publications', api_name:'', name:'Publications'}} />
            )}/>
            {contentTypes.map((c,i)=>(
                <Route path={`/${c.slug}`} render={(props)=>(
                  <SiteFilter {...props}
                    programId={new URLSearchParams(props.location.search).get('program_id')}
                    contentType={c} />
                )}/>
            ))}
          </Switch>
          <ContentList />
        </section>
      </BrowserRouter>
    );
  }
}

const mapStateToProps = (state) => ({
  contentTypes: state.contentTypes.results || []
});

const APP = connect(mapStateToProps)(App);

export default {
  NAME, ID, APP
};
