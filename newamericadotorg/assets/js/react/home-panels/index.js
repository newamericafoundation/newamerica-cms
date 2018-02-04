import { Fetch } from '../components/API';
import { NAME, ID } from './constants';
import { Component } from 'react';
import OurStory from './pages/OurStory';
import ShareOurSpace from './pages/ShareOurSpace';
import PressRoom from './pages/PressRoom';
import OurFunding from './pages/OurFunding';
import Jobs from './pages/Jobs';
import { BrowserRouter as Router, Route } from 'react-router-dom';

const Routes = (props) => (
  <Router>
    <div className="home__panels">
      <Route path="/our-story/" render={(_props)=>( <OurStory {...props} {..._props} /> )} />
      <Route path="/share-our-space/" render={(_props)=>( <ShareOurSpace {...props} {..._props} /> )} />
      <Route path="/press-room/" render={(_props)=>( <PressRoom {...props} {..._props} /> )} />
      <Route path="/our-funding/" render={(_props)=>( <OurFunding {...props} {..._props} /> )} />
      <Route path="/jobs/" render={(_props)=>( <Jobs {...props} {..._props} /> )} />
    </div>
  </Router>
);

class APP extends Component {
  render(){
    let { pageId } = this.props;
    return (
      <Fetch endpoint={`home/${pageId}`}
        fetchOnMount={true}
        name={NAME}
        component={Routes} />
    );
  }
}

export default { APP, ID, NAME };
