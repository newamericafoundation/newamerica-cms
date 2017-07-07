import { Response } from '../../components/API';
import { Component } from 'react';
import { NAME } from '../constants';
import { format as formatDate } from 'date-fns';

class Results extends Component {
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

  componentWillUnmount(){
    this.props.clearResults();
  }

  render(){
    let { response: { results }} = this.props;
    return(
      <div className="search__results">
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
            </div>
            <p className="search__results__item__description no-margin">
              {p.specific.date &&
                <label className={p.specific.description ? 'with-description' : ''}>
                  {formatDate(p.specific.date, 'MMMM D, YYYY')}
                </label>
              }
              {this.cleanDescription(p)}
            </p>
          </div>
        ))}
      </div>
    );
  }
}

const ResultsWrapper = () => (
  <Response name={NAME} component={Results} />
);

export default ResultsWrapper;
