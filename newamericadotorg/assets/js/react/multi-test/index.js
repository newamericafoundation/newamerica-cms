const NAME = 'multiTest';
const ID = 'multi-test';
const MULTI = true;

import { Fetch } from '../components/API';

const post = ({ response: { results }}) => (
  <div>
    <h1>One Multi</h1>
    {results.map((p,i)=>(
      <h4>{p.title}</h4>
    ))}
  </div>
);

const APP = () => (
  <Fetch name={NAME}
    endpoint='post'
    fetchOnMount={true}
    component={post}
    initialQuery={{
      page_size: 5
    }}
  />
);

export default { NAME, ID, APP, MULTI };
