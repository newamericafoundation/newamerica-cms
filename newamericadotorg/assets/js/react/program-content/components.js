import { NAME, IMAGE_RENDITION } from './constants';
import { Component } from 'react';
import { connect } from 'react-redux';
import { Fetch } from '../components/API';
import { format as formatDate } from 'date-fns';
import LoadingIcon from '../components/LoadingIcon';

export const ContentGridItem = ({ item, className, page }) => (
  <div className={`content-grid__item ${className} ${item.story_image? 'with-image' : ''}`}>
      {item.story_image &&
        <div className="content-grid__item__image-wrapper">
          <img src={item.story_image} className="content-grid__item__image" />
        </div>
      }
      <div className="content-grid__item__text">
        <label className="content-grid__item__text__content-type narrow-margin active gray">
          {(page=='homepage' && item.programs[0]) &&
            <a href={item.programs[0].url} className="content-grid__item__text__content-type__program">
              {item.programs[0].name}
            </a>
            }
          {item.content_type.name}
        </label>
        <label className="content-grid__item__text__title md active">
          <a href={item.url} className="content-grid__item__link-wrapper">{item.title}</a>
        </label>
        <p className="content-grid__item__text__description narrow-margin gray">
          <label className="with-description">{formatDate(item.date, 'MMMM D, YYYY')}</label>
          {item.story_excerpt}
        </p>
      </div>
  </div>
);

class ContentGrid extends Component {
  defaultContentType = {title: 'Publications', slug: 'publications'}
  contentType = this.defaultContentType
  render(){
    let { response, content_types, setQueryParam, className, page } = this.props;
    return (
      <section id="publications" className="container--full-width program-block">
      	<h1 className="centered">Recent Publications</h1>
        {content_types.length > 0 &&
          <section className="content-type-filters container--medium inline-toggles-wrapper">
            <div className="inline-toggles">
              <div className={`inline-toggles__item ${response.params.query.content_type=='' ? 'selected' : ''}`}>
                <a onClick={()=>{this.contentType=this.defaultContentType;setQueryParam('content_type', '', true);}}>All</a>
              </div>
              {content_types.filter((c)=>(c.api_name!='indepthproject'&&c.api_name!='weeklyarticle')).map((c)=>(
                <div className={`inline-toggles__item ${response.params.query.content_type==c.api_name ? 'selected' : ''}`}>
                  <a onClick={()=>{this.contentType=c;setQueryParam('content_type', c.api_name, true);}}>{c.title}</a>
                </div>
              ))}
            </div>
          </section>
        }
      	<section className={`program-content-grid container ${className}`}>
          <div className="row">
            {response.results.map((item, i) => (
              <ContentGridItem item={item} page={page} className="col-md-3" />
            ))}
          </div>
          <div className="loading-icon-container"><LoadingIcon /></div>
        </section>
      	<div className="program-block__button-wrapper button-wrapper centered">
      		<a className="button transparent" href={`${location.pathname}${this.contentType.slug}`}>View All {this.contentType.title}</a>
      	</div>
      </section>
    );
  }
}

const mapStateToProps = (state) => ({
  content_types: !state.program.detail.hasResults ? state.contentTypes.results : state.program.detail.results.content_types
});

ContentGrid = connect(mapStateToProps)(ContentGrid);

export class Content extends Component {
  render(){
    let { contentType, programId } = this.props
    let query = {};
    switch(contentType){
      case 'homepage':
        break;
      case 'program':
        query.program_id = programId;
        break;
      case 'subprogram':
        query.project_id = programId;
    }

    return(
      <Fetch name="program.detail"
        fetchOnMount={contentType!='homepage'}
        endpoint={contentType=='program' ? `program/${programId}` : `project/${programId}`}>
        <Fetch
          name='program.content'
          endpoint="post"
          fetchOnMount={true}
          component={ContentGrid}
          showLoading={true}
          transition={true}
          renderIfNoResults={false}
          initialQuery={{
            content_type: '',
            page_size: 8,
            image_rendition: IMAGE_RENDITION,
            ...query
          }}
          page={contentType}
          programId={this.props.programId}/>
      </Fetch>
    );
  }
}
