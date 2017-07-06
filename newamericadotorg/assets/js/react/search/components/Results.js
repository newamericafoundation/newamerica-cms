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
            <p className="search__results__item__description narrow-margin">
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
