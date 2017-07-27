import { Response } from '../../components/API';
import { ContentListItem } from '../../components/Content';
import { NAME } from '../constants';

const ContentList = ({ response: { results }}) => {
  if(results.length===0) return null;
  return (
    <div className="topic__content__list container--medium content-list">
      {results.map((c,i)=>(
        <ContentListItem post={c} />
      ))}
    </div>
  );
}


export default () => (
  <Response name={NAME+'.content'} component={ContentList} />
);
