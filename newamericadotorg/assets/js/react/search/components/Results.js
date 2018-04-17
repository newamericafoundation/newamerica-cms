import { Component } from 'react';
import { NAME } from '../constants';
import { format as formatDate } from 'date-fns';
import LoadingIcon from '../../components/LoadingIcon';

export default class Results extends Component {
  cleanDescription = (p) => {
    let d = p.specific.description;
    if(d) return d.replace(/<(?:.|\n)*?>/gm, '')
  }

  cleanTitle = (p) => {
    let l = p.title.length;
    let title = p.title.substring(0,67);
    if(l > 67) title += ' ...';
    return title;
  }

  getParams = () => {
    let { response: { params }} = this.props;
    let p = new URLSearchParams();

    p.set('query', params.query.query);

    return p.toString();
  }

  componentWillUnmount(){
    this.props.clearResults();
  }

  render(){
    let { response: { results, isFetching, hasResults, hasNext, params }, className } = this.props;
    return(
    <div className={"search__results " + className}>
        {results.map((p,i)=>(
          <div className="search__results__item">
            <label className="lg active search__results__item__title">
              <a href={p.url}>
                {this.cleanTitle(p)}
              </a>
            </label>
            <div className="search__results__item__details">
              {p.specific.programs.length!==0 &&
                <label className="search__results__item__details__program active">
                  <a href={p.specific.programs[0].url}>{p.specific.programs[0].name}</a>
                </label>
              }
              <label className="search__results__item__details__content-type active">
                {p.specific.content_type.name}
              </label>
            </div>{p.specific.authors[0] &&
              <label className="search__results__item__author">
                by {p.specific.authors.map((a,i)=>(
                  <span key={`author-${i}`}>
                    <a href={a.url}>{a.first_name + ' ' + a.last_name}</a>
                    {i<p.specific.authors.length-2 && ', '}
                    {i==p.specific.authors.length-2 && ' and '}
                  </span>
                ))}
              </label>
            }
            <p className="search__results__item__description margin-0">
              {p.specific.date &&
                <label className={p.specific.description ? 'with-description' : ''}>
                  {formatDate(p.specific.date, 'MMMM D, YYYY')}
                </label>
              }
              {this.cleanDescription(p)}
            </p>
          </div>
        ))}
        <div className="loading-icon-container"><LoadingIcon /></div>
        {(results.length===0 && !isFetching && hasResults && params.query.query != '') &&
          <div className="no-results">
            <label className="lg active">No results found</label>
          </div>
        }{hasNext &&
          <div className="search__results__item__see-more">
            <a href={`/search/?${this.getParams()}`} className="button transparent">See more</a>
          </div>
        }
      </div>
    );
  }
}
