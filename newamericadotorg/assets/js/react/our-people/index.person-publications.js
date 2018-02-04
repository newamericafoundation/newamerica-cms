import { Component } from 'react';
import { Fetch } from '../components/API';
import { PERSON_NAME as NAME, PERSON_ID as ID } from './constants';
import {PublicationsList} from '../components/Publications';


const RecentPublications = (props) => (
  <div className="person__recent-publications">
    <div className="section-separator">
      <div className="section-separator__text"><label>Recent Publications</label></div>
      <div className="section-separator__line"></div>
    </div>
    <PublicationsList {...props} />
  </div>
);

class APP extends Component {
  render(){
    let {authorId} = this.props;
    console.log(authorId)
    return (
      <Fetch name={NAME} endpoint={'post'}
        component={RecentPublications}
        fetchOnMount={true}
        renderIfNoResults={false}
        initialQuery={{
          page_size: 4,
          author_id: authorId
        }}/>
    );
  }
}


export default { APP, NAME, ID };
