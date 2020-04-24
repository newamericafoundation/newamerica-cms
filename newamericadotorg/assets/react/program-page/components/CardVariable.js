import React, { Component } from 'react';
import Image from '../../components/Image';

export default class CardVariable extends Component {
  render(){
    let { post, loaded} = this.props;
    return (
      <div className={`card variable`}>
        <a href={post.url} className="row gutter-0">
          {post.story_image &&
          <div className="col-6 col-md-12" style={{overflow: 'hidden'}}>
            <div className="card__image" style={{ paddingBottom: `${post.story_image.height/post.story_image.width*100}%`}}>
              <Image thumbnail={post.story_image_thumbnail.url} image={post.story_image.url} loaded={loaded}/>
            </div>
          </div>}
          <div className={`${post.story_image ? 'col-6' : 'col-12'} col-md-12`}>
            <div className="card__text">
              <h4 className="card__text__title margin-0">
                <span><u dangerouslySetInnerHTML={{ __html: manualBreaks(post.seo_title || post.title) }}/></span>
              </h4>
              <h6 className="card__text__program caption margin-top-10 margin-bottom-0">
                {post.programs ? post.programs[0].name : ''} {post.content_type ? post.content_type.name : ''}
              </h6>
            </div>
          </div>
        </a>
      </div>
    )
  }
}

function manualBreaks(text){
  let len = text.length;
  let t = text.split('');
  let _t = [...t];
  let lastSpace = 0;
  let breakpoints = [115,75,42];
  for(let i=0; i<t.length; i++){
    if(t[i]===' ') lastSpace = i;
    if(breakpoints.indexOf(i)!== -1) _t[lastSpace] = '&nbsp;<span class="br"></span>';
  }

  return _t.join('');
}
