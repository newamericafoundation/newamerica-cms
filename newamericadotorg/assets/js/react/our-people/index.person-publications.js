import { Component } from 'react';
import { Fetch } from '../components/API';
import { PERSON_NAME as NAME, PERSON_ID as ID } from './constants';
import { PublicationsList } from '../components/Publications';


const RecentPublications = (props) => (
  <div className="person__recent-publications">
    <div className="section-separator margin-35">
      <div className="section-separator__text">
        <h6 className="margin-0 inline">Recent Publications</h6>
      </div>
      <div className="section-separator__line"></div>
    </div>
    <PublicationsList {...props} />
  </div>
);

class APP extends Component {
  render(){
    let {authorId} = this.props;
    return (
      <Fetch name={NAME} endpoint={'post'}
        component={RecentPublications}
        fetchOnMount={true}
        renderIfNoResults={false}
        initialQuery={{
          page_size: 4,
          image_rendition: 'fill-300x230',
          author_id: authorId
        }}/>
    );
  }
}


export default { APP, NAME, ID };
