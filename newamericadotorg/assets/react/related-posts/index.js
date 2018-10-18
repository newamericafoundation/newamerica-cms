import React from 'react';
import { Fetch } from '../components/API';
import CardLg from '../program-page/components/CardLg';

const NAME = 'relatedPosts';
const ID = 'related-posts';


const RelatedPosts = ({ response }) => {
  return (
    <div className="container">
      {response.results.map((p,i) => (
        <CardLg post={p} key={`post-${i}`} />
      ))}
    </div>
  );
}


const APP = ({ parentProgramId }) => (
  <Fetch name={NAME} endpoint='post'
    initialQuery={{
      program_id: parentProgramId,
      page_size: 5
    }}
    component={RelatedPosts}
    fetchOnMount={true}
   />
);


export default { APP, NAME, ID };
