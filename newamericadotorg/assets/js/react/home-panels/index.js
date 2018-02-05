import { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { Fetch } from '../components/API';
import { NAME, ID } from './constants';
import OurStory from './pages/OurStory';
import ShareOurSpace from './pages/ShareOurSpace';
import PressRoom from './pages/PressRoom';
import OurFunding from './pages/OurFunding';
import Jobs from './pages/Jobs';
import Programs from './pages/Programs';



class Routes extends Component {
    componentDidMount(){
      let { dispatch } = this.props;
      dispatch({
        type: 'RELOAD_SCROLL_EVENTS',
        component: 'site'
      });
    }
    render(){
      let props = this.props;
      return (
          <div className="home__panels">
            <Route path="/our-story/" render={(_props)=>( <OurStory {...props} {..._props} /> )} />
            <Route path="/share-our-space/" render={(_props)=>( <ShareOurSpace {...props} {..._props} /> )} />
            <Route path="/press-room/" render={(_props)=>( <PressRoom {...props} {..._props} /> )} />
            <Route path="/our-funding/" render={(_props)=>( <OurFunding {...props} {..._props} /> )} />
            <Route path="/jobs/" render={(_props)=>( <Jobs {...props} {..._props} /> )} />
          </div>
      );
    }
}

class APP extends Component {
  render(){
    let { pageId } = this.props;
    return (
      <Router>
        <Switch>
          <Route path="/fellowships/" render={()=>(
            <Fetch endpoint={`program/fellowships`}
              fetchOnMount={true}
              name={NAME}
              component={Programs} />
          )}/>
          <Route path="/programs/" render={()=>(
            <Fetch endpoint={`program`}
              fetchOnMount={true}
              name={NAME}
              component={Programs} />
          )}/>
          <Route path="/(our-story|share-our-space|press-room|our-funding|jobs)/" render={(props)=>(
            <Fetch endpoint={`home/${pageId}`}
              fetchOnMount={true}
              {...props}
              name={NAME}
              component={Routes} />
          )}/>
        </Switch>
      </Router>
    );
  }
}

export default { APP, ID, NAME };
