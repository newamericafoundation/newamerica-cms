import { Component } from 'react';
import { Fetch, Response } from '../../components/API';
import Filters from './PublicationsFilters';
import { format as formatDate } from 'date-fns';

  //
const PublicationListItem = ({ post }) => (
  <div className="card list">
    <a href={post.url}>
      <div className={`card__image ${!post.story_image ? 'no-image' : ''}`}>
        <div className="card__image__background" style={{ backgroundImage: `url(${post.story_image})` }}></div>
      </div>
      </a>
    <div className="card__text">
      <a href={post.url}>
        <label className="card__text__date margin-top-0 block">{formatDate(post.date, 'MMM. Do, YYYY')}</label>
        <label className="card__text__title bold block">{post.title}</label>
      </a>
      {post.authors &&
      <label className="card__text__description subtitle block">
        {post.authors.map((a, i)=>(
          <span>
            <a href={a.url} className="inline">{a.first_name} {a.last_name}</a>
            {i != (post.authors.length-1) &&
              <span> + </span>
            }
          </span>
        ))}
      </label>}
      <a href={post.url}>
        <label className="card__text__program caption margin-bottom-0 block">
          {post.programs[0].name} {post.content_type ? post.content_type.title : ''}
        </label>
      </a>
    </div>
  </div>
);

export const LoadingDots = ({ color='black' }) => (
  <label className={`button--text loading-dots centered ${color} block`}>
    <span>.</span><span>.</span><span>.</span>
  </label>
);

export class PublicationsList extends Component {
  loadMore = () => {
    let { fetchAndAppend, setQueryParam, response } = this.props;
    if(!response.hasNext || response.isFetching) return;
    this.isLoadingMore = true;
    setQueryParam('page', response.page+1);
    fetchAndAppend(this.triggerScrollEvents);
  }

  triggerScrollEvents = () => {
    setTimeout(()=>{
      this.isLoadingMore = false;
      this.props.dispatch({
        type: 'TRIGGER_SCROLL_EVENTS',
        component: 'site'
      });
    });
  }

  render(){
    let { response, fetchAndAppend } = this.props;
    let { results, isFetching, hasNext } = response;
    if(results.length===0 && !isFetching){
      return (
        <label className="bold block centered">No results found</label>
      );
    }

    if(isFetching && !this.isLoadingMore){
      return (
        <div className="program__publications-list-wrapper">
          <div className="program__publications-list margin-top-60">
              <LoadingDots />
          </div>
        </div>
      );
    }

    return (
      <div className="program__publications-list-wrapper">
        <div className="program__publications-list">
            {results.map((post, i ) => (
              <PublicationListItem post={post} />
            ))}
        </div>
        {hasNext &&
        <div className="program__publications-list-load-more container black margin-top-10" onClick={this.loadMore}>
          {!isFetching && <label className="button--text centered white">Load More</label>}
          {isFetching && <LoadingDots color="white" />}
        </div>}
      </div>
    );
  }
}

export default class Publications extends Component {

  render(){
    let { program, history, location } = this.props;
    let params = new URLSearchParams(location.search.replace('?', ''));
    let slug = location.pathname.match(/.+\/(.+)\/$/i)[1];
    let type = program.content_types.find((t)=>(t.slug === slug ));
    return (
      <div className="program__publications row gutter-45 scroll-target margin-top-35" data-scroll-trigger-point="bottom" data-scroll-bottom-offset="65">
        <div className="col-3 program__publications__filter-col">
          <Fetch component={Filters} name="programPage.publications"
            endpoint={'post'}
            fetchOnMount={true}
            program={program}
            history={history}
            location={location}
            initialQuery={{
              program_id: program.id,
              image_rendition: 'max-300x240',
              content_type: type ? type.api_name : '',
              subprogram_id: params.get('subprogramId') || '',
              page_size: 8,
              page: 1
            }}/>
        </div>
        <div className='col-9 program__publications__list-col'>
          <Response name="programPage.publications" component={PublicationsList}/>
        </div>
      </div>
    );
  }
}
